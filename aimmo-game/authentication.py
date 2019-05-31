import os

import kubernetes
import requests


async def initialize_game_token(communicator):
    """Get game token and store it somewhere accessible."""
    if os.environ["WORKER"] == "kubernetes":
        api = kubernetes.client.CoreV1Api()
        game_id = os.environ.get("GAME_ID")

        secret = api.read_namespaced_secret(f"game-{game_id}-token", "default")
        os.environ["TOKEN"] = secret.data["token"]

    await communicator.patch_token({"token": os.environ["TOKEN"]})
