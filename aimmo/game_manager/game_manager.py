import logging
import json

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
    def game_name(game_id: int) -> str:
        """
        Creates a name that will be used as the pod name as well as in other places.

        :param game_id: Integer indicating the GAME_ID of the game.
        :return: A string with the game appended with the id.
        """
        return f"game-{game_id}"

    def create_game_secret(self, game_id: int, token: str):
        game_name = self.game_name(game_id=game_id)
        self.game_secret_manager.create_game_secret(
            game_id=game_id,
            game_name=game_name,
            token=token,
        )

    def create_game_server(self, game_id: int, game_data: dict):
        """
        Creates a game server allocation, a game service and an ingress path.


        Args:
            game_id (int): The GAME_ID of the game.
            game_data (dict): Game data configuration to be passed onto the game server.
        """
        game_name = self.game_name(game_id=game_id)
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
            # TODO: Filter out no-ingress exception on localhost
            pass
            # LOGGER.exception(e)

    def delete_game_server(self, game_id: int) -> dict:
        """
        Delete the game server with the specified game_id and return its game data.

        :param game_id: Integer indicating the ID of the game to delete.
        :returns: A dictionary representing the game data.
        """
        game_name = self.game_name(game_id=game_id)
        try:
            self.game_ingress_manager.remove_game_path_from_ingress(game_name=game_name)
        except ApiException as e:
            LOGGER.exception(e)
        self.game_service_manager.delete_game_service(game_id=game_id)
        return self.game_server_manager.delete_game_server(game_id=game_id)

    def recreate_game_server(self, game_id: int, game_data_updates: dict = None) -> None:
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

        if game_data.get("settings") and isinstance(game_data.get("settings"), str) and game_data.get("worksheet_id"):
            setting = json.loads(game_data["settings"])
            setting["TARGET_NUM_PICKUPS_PER_AVATAR"] = 0 if game_data["worksheet_id"] == "1" else 1.2
            game_data["settings"] = json.dumps(setting)

        game_name = self.game_name(game_id=game_id)
        game_server_name = self.game_server_manager.create_game_server_allocation(
            game_id=game_id,
            game_data=game_data,
        )
        self.game_service_manager.patch_game_service(
            game_id=game_id,
            game_name=game_name,
            game_server_name=game_server_name,
        )
