import os
import secrets

NUM_BYTES_FOR_TOKEN_GENERATOR = 16


def generate_game_token(num_bytes=NUM_BYTES_FOR_TOKEN_GENERATOR):
    """Generate a random token for the game."""
    new_token = secrets.token_urlsafe(nbytes=num_bytes)
    os.environ["TOKEN"] = new_token
    requests.patch(
        game_runner.communicator.django_api_url + "token/", data={"token": new_token}
    )
