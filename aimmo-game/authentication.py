import base64
import logging
import os

from kubernetes.client import CoreV1Api

LOGGER = logging.getLogger(__name__)


def _decode_token_from_secret(secret):
    return base64.b64decode(secret.data["token"]).decode()


async def initialize_game_token(communicator, game_id):
    """Get game token and store it somewhere accessible."""
    api = CoreV1Api()
    secret = api.read_namespaced_secret(f"game-{game_id}-token", "default")
    os.environ["TOKEN"] = _decode_token_from_secret(secret)
    LOGGER.info("Token set!")

    response = await communicator.patch_token({"token": os.environ["TOKEN"]})
    if response.status != 200:
        LOGGER.error(response)
