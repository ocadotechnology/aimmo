import logging
import time

from kubernetes.client import CoreV1Api
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient

from aimmo.app_settings import DJANGO_BASE_URL_FOR_GAME_SERVER
from .constants import AGONES_GROUP, K8S_NAMESPACE

LOGGER = logging.getLogger(__name__)


class GameServerManager:
    def __init__(self) -> None:
        self.api: CoreV1Api = CoreV1Api()
        self.api_client: ApiClient = ApiClient()
        self.custom_objects_api: CustomObjectsApi = CustomObjectsApi(self.api_client)

    def create_game_server_allocation(self, game_id: int, game_data: dict, retry_count: int = 0) -> str:
        game_data["GAME_API_URL"] = f"{DJANGO_BASE_URL_FOR_GAME_SERVER}/kurono/api/games/{game_id}/"

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
        if result["status"]["state"] == "UnAllocated" and retry_count < 10:
            LOGGER.warning(f"Failed to create game, retrying... retry_count={retry_count}")
            time.sleep(5)
            return self.create_game_server_allocation(game_id, game_data, retry_count=retry_count + 1)
        else:
            if result["status"]["state"] == "Allocated":
                LOGGER.info(f"Game {game_id} is now allocated!")
            else:
                LOGGER.error(f"Game {game_id} failed to allocate")
            return result["status"]["gameServerName"]

    def delete_game_server(self, game_id: int) -> dict:
        """
        Delete the game server with the specified game_id and return its game data.

        :param game_id: Integer indicating the ID of the game to delete.
        :returns: A dictionary representing the game data.
        """
        LOGGER.info(f"Deleting game server for game {game_id}")
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
            LOGGER.warning(f"delete_game_server - No game server found with ID {game_id}")
        elif len(game_servers_to_delete) > 1:
            LOGGER.warning(f"delete_game_server - Multiple game servers found with ID {game_id}")

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
        game_data = {k: v for k, v in game_data.items() if not k.startswith(f"{AGONES_GROUP}/")}
        return game_data
