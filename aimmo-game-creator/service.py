#!/usr/bin/env python
import logging
import os

import google.cloud.logging
from google.auth.exceptions import DefaultCredentialsError

from game_manager import GAME_MANAGERS


def main():
    logging.basicConfig(level=logging.DEBUG)
    try:
        logging_client = google.cloud.logging.Client()
        logging_client.get_default_handler()
        logging_client.setup_logging()
    except DefaultCredentialsError:
        logging.info(
            "No google credentials provided, not connecting google logging client"
        )
    game_manager_class = GAME_MANAGERS[os.environ.get("GAME_MANAGER", "local")]
    host = os.environ.get("LOCALHOST_IP", "localhost")
    game_manager = game_manager_class(
        os.environ.get("GAME_API_URL", "http://{}:8000/kurono/api/games/".format(host))
    )
    game_manager.run()


if __name__ == "__main__":
    # Create a place to store game tokens for local mode.
    if not os.path.exists("/tokens"):
        os.makedirs("/tokens")

    with open("/tokens/local_tokens.json", "w+") as f:
        f.write("{}")

    main()
