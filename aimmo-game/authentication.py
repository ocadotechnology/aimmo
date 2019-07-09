import base64
import logging
import os

import kubernetes
import requests
from requests import codes

LOGGER = logging.getLogger(__name__)


def _decode_token_from_secret(secret):
    return base64.b64decode(secret.data["token"]).decode()


async def initialize_game_token(communicator):
    """Get game token and store it somewhere accessible."""
    if os.environ["WORKER"] == "kubernetes":
        kubernetes.config.load_incluster_config()
        api = kubernetes.client.CoreV1Api()
        game_id = os.environ.get("GAME_ID")

        secret = api.read_namespaced_secret(f"game-{game_id}-token", "default")
        os.environ["TOKEN"] = _decode_token_from_secret(secret)
        LOGGER.info("Token set!")

    response = await communicator.patch_token({"token": os.environ["TOKEN"]})
    if response.status != codes["ok"]:
        LOGGER.error(response)
