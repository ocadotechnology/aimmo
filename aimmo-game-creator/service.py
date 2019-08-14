#!/usr/bin/env python
import logging
import os

from game_manager import GAME_MANAGERS


def main():
    logging.basicConfig(level=logging.DEBUG)
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
