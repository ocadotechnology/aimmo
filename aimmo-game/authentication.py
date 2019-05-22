import os

import kubernetes
import requests


def initialize_game_token(communicator):
    """Gets game token and stores it somewhere accesible."""
    if os.environ["WORKER"] == "kubernetes":
        api = kubernetes.client.CoreV1Api()
        game_id = os.environ.get("GAME_ID")

        secret = v1.read_namespaced_secret(f"game-{game_id}-token", "default")
        os.environ["TOKEN"] = secret.data["token"]

    communicator.patch_game({"token": os.environ["TOKEN"]})
