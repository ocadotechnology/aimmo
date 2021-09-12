# This will probably replace the whole aimmo-game-creator at some point.
# For now it just duplicates a part of aimmo-game-creator/game_manager.py in order to recreate a game server.
import logging
import time

import kubernetes
from kubernetes.client import CoreV1Api
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient
from kubernetes.client.rest import ApiException

LOGGER = logging.getLogger(__name__)

K8S_NAMESPACE = "default"
AGONES_GROUP = "agones.dev"


class GameManager:
    def __init__(self) -> None:
        self.api: CoreV1Api = CoreV1Api()
        self.api_client: ApiClient = ApiClient()
        self.custom_objects_api: CustomObjectsApi = CustomObjectsApi(self.api_client)

    @staticmethod
    def create_game_name(game_id: int) -> str:
        """
        Creates a name that will be used as the pod name as well as in other places.

        :param game_id: Integer indicating the GAME_ID of the game.
        :return: A string with the game appended with the id.
        """
        return f"game-{game_id}"

    def patch_game_service(self, game_id, game_server_name):
        patched_service = kubernetes.client.V1Service(
            spec=kubernetes.client.V1ServiceSpec(
                selector={"agones.dev/gameserver": game_server_name}
            )
        )
        self.api.patch_namespaced_service(
            self.create_game_name(game_id), K8S_NAMESPACE, patched_service
        )

    def create_game_server_allocation(
        self, game_id: int, game_data: dict, retry_count: int = 0
    ) -> str:
        result = self.custom_objects_api.create_namespaced_custom_object(
            group="allocation.agones.dev",
            version="v1",
            namespace=K8S_NAMESPACE,
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
                            "game-id": str(game_id),
                        },
                        "annotations": game_data,
                    },
                },
            },
        )
        if result["status"]["state"] == "UnAllocated" and retry_count < 60:
            LOGGER.warning(
                f"Failed to create game, retrying... retry_count={retry_count}"
            )
            time.sleep(5)
            return self.create_game_server_allocation(
                game_id, game_data, retry_count=retry_count + 1
            )
        else:
            return result["status"]["gameServerName"]

    def delete_game_server(self, game_id: int) -> dict:
        """
        Delete the game server with the specified game_id and return its game data.

        :param game_id: Integer indicating the ID of the game to delete.
        :returns: A dictionary representing the game data.
        """
        game_data = {}
        result = self.custom_objects_api.list_namespaced_custom_object(
            group=AGONES_GROUP,
            version="v1",
            namespace=K8S_NAMESPACE,
            plural="gameservers",
            label_selector=f"game-id={game_id}",
        )
        game_servers_to_delete = result["items"]

        if len(game_servers_to_delete) == 0:
            LOGGER.warning(
                f"delete_game_server - No game server found with ID {game_id}"
            )
        elif len(game_servers_to_delete) > 1:
            LOGGER.warning(
                f"delete_game_server - Multiple game servers found with ID {game_id}"
            )

        for game_server in game_servers_to_delete:
            name = game_server["metadata"]["name"]
            game_data.update(game_server["metadata"]["annotations"])
            self.custom_objects_api.delete_namespaced_custom_object(
                group=AGONES_GROUP,
                version="v1",
                namespace=K8S_NAMESPACE,
                plural="gameservers",
                name=name,
            )

        # Remove agones specific annotations from game_data
        game_data = {
            k: v for k, v in game_data.items() if not k.startswith(f"{AGONES_GROUP}/")
        }
        return game_data

    def recreate_game_server(
        self, game_id: int, game_data_updates: dict = None
    ) -> None:
        """
        Recreate a game server with the specified game_id and optionally update its game data.

        :param game_id: Integer indicating the ID of the game to recreate.
        :param game_data_updates: Optional, a dictionary with game data updates.
        :returns: None
        """
        if game_data_updates is None:
            game_data_updates = {}

        game_data = self.delete_game_server(game_id=game_id)
        game_data.update(game_data_updates)
        game_server_name = self.create_game_server_allocation(
            game_id=game_id, game_data=game_data
        )
        self.patch_game_service(game_id=game_id, game_server_name=game_server_name)

    def create_game_secret(self, game_id, token):
        name = self.create_game_name(game_id) + "-token"
        body = kubernetes.client.V1Secret(
            kind="Secret",
            string_data={"token": token},
            metadata=kubernetes.client.V1ObjectMeta(
                name=name,
                namespace=K8S_NAMESPACE,
                labels={"game_id": str(game_id), "app": "aimmo-game"},
            ),
        )
        try:
            self.api.read_namespaced_secret(name, K8S_NAMESPACE)
        except ApiException:
            try:
                self.api.create_namespaced_secret(namespace=K8S_NAMESPACE, body=body)
            except ApiException:
                LOGGER.exception("Exception when calling create_namespaced_secret")
        else:
            try:
                self.api.patch_namespaced_secret(
                    name=name, namespace=K8S_NAMESPACE, body=body
                )
            except ApiException:
                LOGGER.exception("Exception when calling patch_namespaced_secret")

    def delete_game_secret(self, game_id):
        app_label = "app=aimmo-game"
        game_label = "game_id={}".format(game_id)

        resources = self.api.list_namespaced_secret(
            namespace=K8S_NAMESPACE, label_selector=",".join([app_label, game_label])
        )

        for resource in resources.items:
            LOGGER.info("Removing game secret: {}".format(resource.metadata.name))
            self.api.delete_namespaced_secret(
                name=resource.metadata.name, namespace=K8S_NAMESPACE
            )
