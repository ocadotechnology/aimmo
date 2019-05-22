import os

import kubernetes
import requests


def get_game_token(django_api_url):
    """Gets game token and stores it somewhere accesible."""
    if os.environ["WORKER"] == "kubernetes":
        api = kubernetes.client.CoreV1Api()
        game_id = os.environ.get("GAME_ID")

        secret = v1.read_namespaced_secret(f"game-{game_id}-token", "default")
        os.environ["TOKEN"] = secret.data["token"]

    return requests.patch(
        django_api_url + "token/",
        headers={"Game-token": os.environ["TOKEN"]},
        data={"token": os.environ["TOKEN"]},
    )
