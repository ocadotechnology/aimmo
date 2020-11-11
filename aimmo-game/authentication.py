import base64
import logging
import os

import kubernetes
import requests
from requests import codes
from kubernetes.config import load_incluster_config, load_kube_config

LOGGER = logging.getLogger(__name__)


def _decode_token_from_secret(secret):
    return base64.b64decode(secret.data["token"]).decode()


async def initialize_game_token(communicator, game_id):
    """Get game token and store it somewhere accessible."""
    if os.environ.get("WORKER") == "kubernetes":
        load_incluster_config()
        api = kubernetes.client.CoreV1Api()

        secret = api.read_namespaced_secret(f"game-{game_id}-token", "default")
        os.environ["TOKEN"] = _decode_token_from_secret(secret)
        LOGGER.info("Token set!")

    response = await communicator.patch_token({"token": os.environ["TOKEN"]})
    if response.status != codes["ok"]:
        LOGGER.error(response)
