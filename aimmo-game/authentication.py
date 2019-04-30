import os
import secrets

import requests

NUM_BYTES_FOR_TOKEN_GENERATOR = 16


def generate_game_token(django_api_url, num_bytes=NUM_BYTES_FOR_TOKEN_GENERATOR):
    """Generate a random token for the game."""
    new_token = secrets.token_urlsafe(nbytes=num_bytes)
    os.environ["TOKEN"] = new_token
    requests.patch(django_api_url + "token/", data={"token": new_token})
