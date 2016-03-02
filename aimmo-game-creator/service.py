#!/usr/bin/env python

import logging
from pykube import HTTPClient
from pykube import KubeConfig
from pykube import ReplicationController
import time

LOGGER = logging.getLogger(__name__)

def create_game(api, name, environment_variables):
    rc = ReplicationController(
        api,
        {
            'kind': 'ReplicationController',
            'apiVersion': 'v1',
            'metadata': {
                'name': name,
                'namespace': 'default',
                'labels': {
                    'app': 'aimmo-game',
                    'game': name,
                },
            },
            'spec': {
                'replicas': 1,
                'selector': {
                    'app': 'aimmo-game',
                    'game': name,
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': 'aimmo-game',
                            'game': name,
                        },
                    },
                    'spec': {
                        'containers': [
                            {
                                'env': [
                                    {
                                        'name': env_name,
                                        'value': env_value,
                                    } for env_name, env_value in environment_variables.items()
                                ],
                                'image': 'ocadotechnology/aimmo-game:latest',
                                'ports': [
                                    {
                                        'containerPort': 80,
                                    },
                                ],
                                'name': 'aimmo-game',
                            },
                        ],
                    },
                },
            },
        },
    )

    rc.create()


def get_games():
    return {
        'main': {
            'VAR1': 'VAL1',
        }
    }


def maintain_games(api, games):
    current_game_names = set()
    for game in ReplicationController.objects(api).filter(selector={'app': 'aimmo-game'}):
        current_game_names.add(game.name)
        if game.name not in games:
            LOGGER.info("Deleting game %s", game.name)
            game.delete()
    for game_id, game_config in games.items():
        if game_id not in current_game_names:
            LOGGER.info("Creating game %s", game_id)
            create_game(api, game_id, game_config)


def main():
    logging.basicConfig(level=logging.DEBUG)
    api = HTTPClient(KubeConfig.from_service_account())
    while True:
        games = get_games()
        maintain_games(api, games)
        time.sleep(5)


if __name__ == '__main__':
    main()
