# This will probably replace the whole aimmo-game-creator at some point.
# For now it just duplicates a part of aimmo-game-creator/game_manager.py in order to recreate a game server.
import logging

from kubernetes.client import CoreV1Api
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient
from kubernetes.client.exceptions import ApiException

from .game_ingress_manager import GameIngressManager
from .game_secret_manager import GameSecretManager
from .game_server_manager import GameServerManager
from .game_service_manager import GameServiceManager

LOGGER = logging.getLogger(__name__)


class GameManager:
    def __init__(
        self,
        game_service_manager: GameServiceManager = GameServiceManager(),
        game_server_manager: GameServerManager = GameServerManager(),
        game_secret_manager: GameSecretManager = GameSecretManager(),
        game_ingress_manager: GameIngressManager = GameIngressManager(),
    ) -> None:
        self.api: CoreV1Api = CoreV1Api()
        self.api_client: ApiClient = ApiClient()
        self.custom_objects_api: CustomObjectsApi = CustomObjectsApi(self.api_client)
        self.game_service_manager = game_service_manager
        self.game_server_manager = game_server_manager
        self.game_secret_manager = game_secret_manager
        self.game_ingress_manager = game_ingress_manager

    @staticmethod
    def create_game_name(game_id: int) -> str:
        """
        Creates a name that will be used as the pod name as well as in other places.

        :param game_id: Integer indicating the GAME_ID of the game.
        :return: A string with the game appended with the id.
        """
        return f"game-{game_id}"

    def create_game_secret(self, game_id: int, token: str):
        game_name = self.create_game_name(game_id=game_id)
        self.game_secret_manager.create_game_secret(
            game_id=game_id,
            game_name=game_name,
            token=token,
        )

    def create_game_server(self, game_id: int, game_data: dict):
        game_name = self.create_game_name(game_id=game_id)
        game_server_name = self.game_server_manager.create_game_server_allocation(
            game_id=game_id,
            game_data=game_data,
        )
        self.game_service_manager.create_game_service(
            game_id=game_id,
            game_name=game_name,
            game_server_name=game_server_name,
        )
        try:
            self.game_ingress_manager.add_game_path_to_ingress(game_name=game_name)
        except ApiException as e:
            LOGGER.exception(e)

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
        Used for recreating games when switching worksheets.

        :param game_id: Integer indicating the ID of the game to recreate.
        :param game_data_updates: Optional, a dictionary with game data updates.
        :returns: None
        """
        if game_data_updates is None:
            game_data_updates = {}

        game_data = self.delete_game_server(game_id=game_id)

        game_data.update(game_data_updates)

        game_name = self.create_game_name(game_id=game_id)
        game_server_name = self.game_server_manager.create_game_server_allocation(
            game_id=game_id,
            game_data=game_data,
        )
        self.game_service_manager.patch_game_service(
            game_id=game_id,
            game_name=game_name,
            game_server_name=game_server_name,
        )
