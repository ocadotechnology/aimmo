# This will probably replace the whole aimmo-game-creator at some point.
# For now it just duplicates a part of aimmo-game-creator/game_manager.py in order to recreate a game server.
from game_manager.game_server_manager import GameServerManager
from .game_service_manager import GameServiceManager
import logging

import kubernetes
from kubernetes.client import CoreV1Api
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient
from kubernetes.client.rest import ApiException

from game_manager import K8S_NAMESPACE, AGONES_GROUP

LOGGER = logging.getLogger(__name__)


class GameManager:
    def __init__(
        self,
        game_service_manager: GameServiceManager = GameServiceManager(),
        game_server_manager: GameServerManager = GameServerManager(),
    ) -> None:
        self.api: CoreV1Api = CoreV1Api()
        self.api_client: ApiClient = ApiClient()
        self.custom_objects_api: CustomObjectsApi = CustomObjectsApi(self.api_client)
        self.game_service_manager = game_service_manager
        self.game_server_manager = game_server_manager

    @staticmethod
    def create_game_name(game_id: int) -> str:
        """
        Creates a name that will be used as the pod name as well as in other places.

        :param game_id: Integer indicating the GAME_ID of the game.
        :return: A string with the game appended with the id.
        """
        return f"game-{game_id}"

    def delete_game_server(self, game_id: int) -> dict:
        """
        Delete the game server with the specified game_id and return its game data.

        :param game_id: Integer indicating the ID of the game to delete.
        :returns: A dictionary representing the game data.
        """
        return self.game_server_manager.delete_game_server(game_id=game_id)

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
        game_server_name = self.game_server_manager.create_game_server_allocation(
            game_id=game_id,
            game_data=game_data,
        )
        game_name = self.create_game_name(game_id=game_id)
        self.game_service_manager.patch_game_service(
            game_id=game_id,
            game_name=game_name,
            game_server_name=game_server_name,
        )

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
