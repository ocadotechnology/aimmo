import logging
import secrets
import time
from abc import ABCMeta, abstractmethod
from concurrent import futures
from enum import Enum

import kubernetes
import requests
from eventlet.semaphore import Semaphore
from kubernetes.client import CoreV1Api
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient
from kubernetes.client.rest import ApiException

from kube_components import TokenSecretCreator

LOGGER = logging.getLogger(__name__)

K8S_NAMESPACE = "default"
NUM_BYTES_FOR_TOKEN_GENERATOR = 16
TOKEN_MAX_LENGTH = 24


class _GameManagerData(object):
    """This class is thread safe"""

    def __init__(self):
        self._games = set()
        self._lock = Semaphore()

    def _add_game(self, game_id):
        assert self._lock.locked
        self._games.add(game_id)

    def _remove_game(self, game_id):
        assert self._lock.locked
        self._games.remove(game_id)

    def add_new_games(self, all_games):
        with self._lock:
            new_games = frozenset(all_games) - self._games
            for n in new_games:
                self._add_game(n)
            return new_games

    def remove_unknown_games(self, known_games):
        with self._lock:
            unknown_games = self._games - frozenset(known_games)
            for u in unknown_games:
                self._remove_game(u)
            return unknown_games

    def remove_stopped_games(self, stopped_games):
        with self._lock:
            for s in stopped_games:
                self._remove_game(s)
            return stopped_games

    def get_games(self):
        with self._lock:
            for g in self._games:
                yield g


class GameStatus(Enum):
    RUNNING = "r"
    PAUSED = "p"
    STOPPED = "s"


class GameManager(object):
    """Methods of this class must be thread safe unless explicitly stated"""

    __metaclass__ = ABCMeta
    daemon = True

    def __init__(self, games_url):
        self._data = _GameManagerData()
        self.games_url = games_url
        super(GameManager, self).__init__()

    def _generate_game_token(self):
        token = secrets.token_urlsafe(nbytes=NUM_BYTES_FOR_TOKEN_GENERATOR)
        # Max length of the auth_token field in the models
        token = token[:TOKEN_MAX_LENGTH] if len(token) > TOKEN_MAX_LENGTH else token
        return token

    @abstractmethod
    def create_game(self, game_id, game_data):
        """Creates a new game"""

        raise NotImplementedError

    @abstractmethod
    def delete_game(self, game_id):
        """Deletes the given game"""

        raise NotImplementedError

    def recreate_game(self, game_to_add):
        """Deletes and recreates the given game"""
        game_id, game_data = game_to_add
        LOGGER.info("Deleting game {}".format(game_id))
        try:
            self.delete_game(game_id)
        except Exception as ex:
            LOGGER.error("Failed to delete game {}".format(game_id))
            LOGGER.exception(ex)

        LOGGER.info("Recreating game {}".format(game_id))
        try:
            game_data["GAME_API_URL"] = "{}{}/".format(self.games_url, game_id)
            self.create_game(game_id, game_data)
        except Exception as ex:
            LOGGER.error("Failed to create game {}".format(game_id))
            LOGGER.exception(ex)

    def update(self):
        try:
            LOGGER.info("Waking up")
            games = requests.get(self.games_url).json()
            LOGGER.debug(f"Received Games: {games}")
        except (requests.RequestException, ValueError) as ex:
            LOGGER.error("Failed to obtain game data")
            LOGGER.exception(ex)
        else:
            games_to_add = {
                id: games[id]
                for id in self._data.add_new_games(games)
                if games[id]["status"] != GameStatus.STOPPED.value
            }

            # Add missing games
            self._parallel_map(self.recreate_game, games_to_add.items())
            # Delete extra games
            known_games = set(games.keys())
            stopped_games = set(
                id
                for id in games.keys()
                if games[id]["status"] == GameStatus.STOPPED.value
            )
            removed_game_ids = self._data.remove_unknown_games(known_games).union(
                self._data.remove_stopped_games(stopped_games)
            )
            self._parallel_map(self.delete_game, removed_game_ids)

    def get_persistent_state(self, player_id):
        """Get the persistent state of a game"""

        return None

    def run(self):
        while True:
            self.update()
            LOGGER.info("Sleeping")
            time.sleep(1)

    def _parallel_map(self, func, iterable_args):
        with futures.ThreadPoolExecutor() as executor:
            _ = executor.map(func, iterable_args)


class KubernetesGameManager(GameManager):
    """Manages games running on Kubernetes cluster"""

    def __init__(self, *args, **kwargs):
        self.networking_api = kubernetes.client.NetworkingV1beta1Api()
        self.api: CoreV1Api = kubernetes.client.CoreV1Api()
        self.secret_creator = TokenSecretCreator()
        self.api_client: ApiClient = ApiClient()
        self.custom_objects_api: CustomObjectsApi = CustomObjectsApi(self.api_client)

        super(KubernetesGameManager, self).__init__(*args, **kwargs)
        self._create_ingress_paths_for_existing_games()

    def _create_ingress_paths_for_existing_games(self):
        games = self._data.get_games()
        for game_id in games:
            self._add_path_to_ingress(game_id)

    @staticmethod
    def _create_game_name(game_id):
        """
        Creates a name that will be used as the pod name as well as in other places.
        :param game_id: Integer indicating the GAME_ID of the game.
        :return: A string with the game appended with the id.
        """
        return "game-{}".format(game_id)

    def _add_path_to_ingress(self, game_id):
        game_name = KubernetesGameManager._create_game_name(game_id)
        backend = kubernetes.client.NetworkingV1beta1IngressBackend(game_name, 80)
        path = kubernetes.client.NetworkingV1beta1HTTPIngressPath(
            backend, f"/{game_name}(/|$)(.*)"
        )

        patch = [{"op": "add", "path": "/spec/rules/0/http/paths/-", "value": path}]

        self.networking_api.patch_namespaced_ingress("aimmo-ingress", "default", patch)

    def _remove_path_from_ingress(self, game_id):
        game_name = KubernetesGameManager._create_game_name(game_id)
        backend = kubernetes.client.NetworkingV1beta1IngressBackend(game_name, 80)
        path = kubernetes.client.NetworkingV1beta1HTTPIngressPath(
            backend, f"/{game_name}(/|$)(.*)"
        )
        ingress = self.networking_api.list_namespaced_ingress("default").items[0]
        paths = ingress.spec.rules[0].http.paths
        try:
            index_to_delete = paths.index(path)
        except ValueError:
            return

        patch = [
            {
                "op": "remove",
                "path": "/spec/rules/0/http/paths/{}".format(index_to_delete),
            }
        ]

        self.networking_api.patch_namespaced_ingress("aimmo-ingress", "default", patch)

    def _create_game_service(self, game_id, game_server_name):
        service_manifest = kubernetes.client.V1ServiceSpec(
            selector={"agones.dev/gameserver": game_server_name},
            ports=[
                kubernetes.client.V1ServicePort(
                    name="tcp", protocol="TCP", port=80, target_port=5000
                )
            ],
        )

        service_metadata = kubernetes.client.V1ObjectMeta(
            name=KubernetesGameManager._create_game_name(game_id),
            labels={"app": "aimmo-game", "game_id": game_id},
        )

        service = kubernetes.client.V1Service(
            metadata=service_metadata, spec=service_manifest
        )
        self.api.create_namespaced_service(K8S_NAMESPACE, service)

    def _delete_game_service(self, game_id):
        app_label = "app=aimmo-game"
        game_label = "game_id={}".format(game_id)

        resources = self.api.list_namespaced_service(
            namespace=K8S_NAMESPACE, label_selector=",".join([app_label, game_label])
        )

        for resource in resources.items:
            LOGGER.info("Removing service: {}".format(resource.metadata.name))
            self.api.delete_namespaced_service(resource.metadata.name, K8S_NAMESPACE)

    def _create_game_secret(self, game_id):
        name = KubernetesGameManager._create_game_name(game_id) + "-token"
        try:
            self.api.read_namespaced_secret(name, K8S_NAMESPACE)
        except ApiException:
            data = {"token": self._generate_game_token()}
            self.secret_creator.create_secret(name, K8S_NAMESPACE, data)

    def _delete_game_secret(self, game_id):
        app_label = "app=aimmo-game"
        game_label = "game_id={}".format(game_id)

        resources = self.api.list_namespaced_secret(
            namespace=K8S_NAMESPACE, label_selector=",".join([app_label, game_label])
        )

        for resource in resources.items:
            LOGGER.info("Removing game secret: {}".format(resource.metadata.name))
            self.api.delete_namespaced_secret(resource.metadata.name, K8S_NAMESPACE)

    def _create_game_server_allocation(
        self, game_id: int, worksheet_id: int, retry_count: int = 0
    ) -> str:
        result = self.custom_objects_api.create_namespaced_custom_object(
            group="allocation.agones.dev",
            version="v1",
            namespace="default",
            plural="gameserverallocations",
            body={
                "apiVersion": "allocation.agones.dev/v1",
                "kind": "GameServerAllocation",
                "metadata": {"generateName": "game-allocation-"},
                "spec": {
                    "required": {"matchLabels": {"agones.dev/fleet": "aimmo-game"}},
                    "scheduling": "Packed",
                    "metadata": {
                        "labels": {
                            "game-id": game_id,
                            "worksheet_id": worksheet_id,
                        },
                        "annotations": {
                            "game-api-url": f"{self.games_url}{game_id}/",
                        },
                    },
                },
            },
        )
        if result["status"]["state"] == "UnAllocated" and retry_count < 5:
            LOGGER.warning(
                f"Failed to create game, retrying... retry_count={retry_count}"
            )
            time.sleep(5)
            return self._create_game_server_allocation(
                game_id, worksheet_id, retry_count=retry_count + 1
            )
        else:
            return result["status"]["gameServerName"]

    def _delete_game_server(self, game_id):
        result = self.custom_objects_api.list_namespaced_custom_object(
            group="agones.dev",
            version="v1",
            namespace="default",
            plural="gameservers",
            label_selector=f"game-id={game_id}",
        )
        game_servers_to_delete = result["items"]
        for game_server in game_servers_to_delete:
            name = game_server["metadata"]["name"]
            self.custom_objects_api.delete_namespaced_custom_object(
                group="agones.dev",
                version="v1",
                namespace="default",
                plural="gameservers",
                name=name,
            )

    def create_game(self, game_id, game_data):
        self._create_game_secret(game_id)
        game_server_name = self._create_game_server_allocation(
            game_id, game_data["worksheet_id"]
        )
        self._create_game_service(game_id, game_server_name)
        self._add_path_to_ingress(game_id)
        LOGGER.info("Game started - {}".format(game_id))

    def delete_game(self, game_id):
        self._remove_path_from_ingress(game_id)
        self._delete_game_service(game_id)
        self._delete_game_server(game_id)
        self._delete_game_secret(game_id)


GAME_MANAGERS = {"kubernetes": KubernetesGameManager}
