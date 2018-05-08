#!/usr/bin/env python
import logging
import os

from game_manager import GAME_MANAGERS


def main():
    logging.basicConfig(level=logging.DEBUG)
    GameManagerClass = GAME_MANAGERS[os.environ.get('GAME_MANAGER', 'local')]
    game_manager = GameManagerClass(os.environ.get('GAME_API_URL',
                                        'http://localhost:8000/players/api/games/'))
    game_manager.run()


if __name__ == '__main__':
    main()
