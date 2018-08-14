import logging
import os
import subprocess
import time
from abc import ABCMeta, abstractmethod

import requests
from eventlet.greenpool import GreenPool
from eventlet.semaphore import Semaphore
import kubernetes


LOGGER = logging.getLogger(__name__)

K8S_NAMESPACE = 'default'


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

    def get_games(self):
        with self._lock:
            for g in self._games:
                yield g


class GameManager(object):
    """Methods of this class must be thread safe unless explicitly stated"""
    __metaclass__ = ABCMeta
    daemon = True

    def __init__(self, games_url):
        self._data = _GameManagerData()
        self.games_url = games_url
        self._pool = GreenPool(size=3)
        super(GameManager, self).__init__()

    @abstractmethod
    def create_game(self, game_id, game_data):
        """Creates a new game"""

        raise NotImplemented

    @abstractmethod
    def delete_game(self, game_id):
        """Deletes the given game"""

        raise NotImplemented

    def recreate_game(self, game_id, game_data):
        """Deletes and recreates the given game"""
        LOGGER.info("Deleting game {}".format(game_data["name"]))
        try:
            self.delete_game(game_id)
        except Exception as ex:
            LOGGER.error("Failed to delete game {}".format(game_data["name"]))
            LOGGER.exception(ex)

        LOGGER.info("Recreating game {}".format(game_data["name"]))
        try:
            game_data["GAME_API_URL"] = "{}{}/".format(self.games_url, game_id)
            self.create_game(game_id, game_data)
        except Exception as ex:
            LOGGER.error("Failed to create game {}".format(game_data["name"]))
            LOGGER.exception(ex)

    def update(self):
        try:
            LOGGER.info("Waking up")
            games = requests.get(self.games_url).json()
        except (requests.RequestException, ValueError) as ex:
            LOGGER.error("Failed to obtain game data")
            LOGGER.exception(ex)
        else:
            games_to_add = {
                id: games[id]
                for id in self._data.add_new_games(games.keys())
            }
            LOGGER.debug("Need to add games: {}".format(games_to_add))

            # Add missing games
            self._parallel_map(self.recreate_game, games_to_add.keys(), games_to_add.values())

            # Delete extra games
            known_games = set(games.keys())
            removed_game_ids = self._data.remove_unknown_games(known_games)
            LOGGER.debug("Removing games: {}".format(removed_game_ids))
            self._parallel_map(self.delete_game, removed_game_ids)

    def get_persistent_state(self, player_id):
        """Get the persistent state of a game"""

        return None

    def run(self):
        while True:
            self.update()
            LOGGER.info("Sleeping")
            time.sleep(10)

    def _parallel_map(self, func, *iterable_args):
        list(self._pool.imap(func, *iterable_args))


class LocalGameManager(GameManager):
    """Manages games running on local host"""

    host = "127.0.0.1"
    game_directory = os.path.join(
        os.path.dirname(__file__),
        "../aimmo-game/",
    )
    game_service_path = os.path.join(game_directory, "service.py")

    def __init__(self, *args, **kwargs):
        self.games = {}
        super(LocalGameManager, self).__init__(*args, **kwargs)

    def create_game(self, game_id, game_data):
        assert(game_id not in self.games)
        port = str(6001 + int(game_id) * 1000)
        process_args = [
            "python",
            self.game_service_path,
            self.host,
            port,
        ]
        env = os.environ.copy()
        game_data = {str(k): str(v) for k, v in game_data.items()}
        env.update(game_data)
        self.games[game_id] = subprocess.Popen(process_args, cwd=self.game_directory, env=env)
        game_url = "http://{}:{}".format(self.host, port)
        LOGGER.info("Game started - {}, listening at {}".format(game_id, game_url))

    def delete_game(self, game_id):
        if game_id in self.games:
            self.games[game_id].kill()
            del self.games[game_id]


class KubernetesGameManager(GameManager):
    """Manages games running on Kubernetes cluster"""

    def __init__(self, *args, **kwargs):
        kubernetes.config.load_incluster_config()
        self.extension_api = kubernetes.client.ExtensionsV1beta1Api()
        self.api = kubernetes.client.CoreV1Api()

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

    def _make_rc(self, environment_variables, game_id):
        container = kubernetes.client.V1Container(
            env=[kubernetes.client.V1EnvVar(
                        name=env_name,
                        value=env_value) for env_name, env_value in environment_variables.items()] +
                [kubernetes.client.V1EnvVar(
                    name='POD_NAME',
                    value_from=kubernetes.client.V1EnvVarSource(
                        field_ref=kubernetes.client.V1ObjectFieldSelector(field_path='metadata.name')))],
            image='ocadotechnology/aimmo-game:{}'.format(os.environ.get('IMAGE_SUFFIX', 'latest')),
            ports=[kubernetes.client.V1ContainerPort(container_port=5000)],
            name='aimmo-game',
            resources=kubernetes.client.V1ResourceRequirements(
                        limits={'cpu': '300m', 'memory': '128Mi'},
                        requests={'cpu': '10m', 'memory': '64Mi'}),
            security_context=kubernetes.client.V1SecurityContext(
                capabilities=kubernetes.client.V1Capabilities(
                    drop=['all'],
                    add=['NET_BIND_SERVICE'])))

        pod_manifest = kubernetes.client.V1PodSpec(containers=[container])
        pod_metadata = kubernetes.client.V1ObjectMeta(labels={'app': 'aimmo-game', 'game_id': game_id})
        pod_template_manifest = kubernetes.client.V1PodTemplateSpec(spec=pod_manifest, metadata=pod_metadata)

        rc_manifest = kubernetes.client.V1ReplicationControllerSpec(
            template=pod_template_manifest,
            selector={'app': 'aimmo-game',
                      'game_id': game_id},
            replicas=1)

        rc_metadata = kubernetes.client.V1ObjectMeta(
            name=KubernetesGameManager._create_game_name(game_id),
            namespace=K8S_NAMESPACE,
            labels={'app': 'aimmo-game', 'game_id': game_id})

        return kubernetes.client.V1ReplicationController(spec=rc_manifest, metadata=rc_metadata)

    def _create_game_rc(self, game_id, environment_variables):
        environment_variables['SOCKETIO_RESOURCE'] = KubernetesGameManager._create_game_name(game_id)
        environment_variables['GAME_ID'] = game_id
        environment_variables['GAME_URL'] = 'http://game-{}'.format(game_id)
        environment_variables['IMAGE_SUFFIX'] = os.environ.get('IMAGE_SUFFIX', 'latest')
        environment_variables['K8S_NAMESPACE'] = K8S_NAMESPACE

        rc = self._make_rc(environment_variables, game_id)
        self.api.create_namespaced_replication_controller(K8S_NAMESPACE, rc)

    def _make_service(self, game_id):
        service_manifest = kubernetes.client.V1ServiceSpec(
            selector={'app': 'aimmo-game', 'game_id': game_id},
            ports=[kubernetes.client.V1ServicePort(protocol='TCP', port=80, target_port=5000)],
            type='NodePort')

        service_metadata = kubernetes.client.V1ObjectMeta(
            name=KubernetesGameManager._create_game_name(game_id),
            labels={'app': 'aimmo-game', 'game_id': game_id})

        return kubernetes.client.V1Service(metadata=service_metadata, spec=service_manifest)

    def _create_game_service(self, game_id):
        service = self._make_service(game_id)
        self.api.create_namespaced_service(K8S_NAMESPACE, service)

    def _add_path_to_ingress(self, game_id):
        backend = kubernetes.client.V1beta1IngressBackend(KubernetesGameManager._create_game_name(game_id), 80)
        path = kubernetes.client.V1beta1HTTPIngressPath(backend,
                                                        "/{}".format(KubernetesGameManager._create_game_name(game_id)))

        patch = [
            {
                "op": "add",
                "path": "/spec/rules/0/http/paths/-",
                "value": path
            }
        ]

        self.extension_api.patch_namespaced_ingress("aimmo-ingress", "default", patch)

    def _remove_path_from_ingress(self, game_id):
        backend = kubernetes.client.V1beta1IngressBackend(KubernetesGameManager._create_game_name(game_id), 80)
        path = kubernetes.client.V1beta1HTTPIngressPath(backend,
                                                        "/{}".format(KubernetesGameManager._create_game_name(game_id)))
        ingress = self.extension_api.list_namespaced_ingress("default").items[0]
        paths = ingress.spec.rules[0].http.paths
        try:
            index_to_delete = paths.index(path)
        except ValueError:
            return

        patch = [
            {
                "op": "remove",
                "path": "/spec/rules/0/http/paths/{}".format(index_to_delete)
            }
        ]

        self.extension_api.patch_namespaced_ingress("aimmo-ingress", "default", patch)

    def _remove_resources(self, game_id, resource_type):
        resource_functions = {'Pod': (self.api.list_namespaced_pod, self.api.delete_namespaced_pod),
                              'ReplicationController': (self.api.list_namespaced_replication_controller,
                                                        self.api.delete_namespaced_replication_controller),
                              'Service': (self.api.list_namespaced_service, self.api.delete_namespaced_service)}

        list_resource_function, delete_resource_function = resource_functions[resource_type]

        app_label = 'app=aimmo-game'
        game_label = 'game_id={}'.format(game_id)

        resources = list_resource_function(namespace=K8S_NAMESPACE,
                                           label_selector=','.join([app_label, game_label]))

        for resource in resources.items:
            LOGGER.info('Removing: {}'.format(resource.metadata.name))
            delete_resource_function(resource.metadata.name, K8S_NAMESPACE, kubernetes.client.V1DeleteOptions())

    def create_game(self, game_id, game_data):
        self._create_game_service(game_id)
        self._create_game_rc(game_id, game_data)
        self._add_path_to_ingress(game_id)
        LOGGER.info("Game started - {}".format(game_id))

    def delete_game(self, game_id):
        self._remove_path_from_ingress(game_id)
        self._remove_resources(game_id, 'ReplicationController')
        self._remove_resources(game_id, 'Pod')
        self._remove_resources(game_id, 'Service')


GAME_MANAGERS = {
    "local": LocalGameManager,
    "kubernetes": KubernetesGameManager,
}
