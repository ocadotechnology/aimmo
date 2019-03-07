import itertools
import logging
import os
import docker
import json

from .worker import Worker

LOGGER = logging.getLogger(__name__)


class LocalWorker(Worker):
    """Relies on them already being created already."""

    host = os.environ.get('LOCALHOST_IP', '127.0.0.1')
    worker_directory = os.path.join(
        os.path.dirname(__file__),
        '../../../aimmo-game-workers/',
    )

    def __init__(self, *args, **kwargs):
        self.game_id = os.environ['GAME_ID']
        self.port_counter = itertools.count(1989 + int(self.game_id) * 10000)
        self.client = docker.from_env()
        super(LocalWorker, self).__init__(*args, **kwargs)

    def _create_worker(self):
        port = next(self.port_counter)

        template_string = os.environ.get('CONTAINER_TEMPLATE')
        if template_string:
            template = json.loads(template_string)
        else:
            template = {
                'environment': {}
            }
        data_url = 'http://{}:{}/player/{}'.format(self.host, self.port, self.player_id)
        template['environment']['DATA_URL'] = data_url
        template['environment']['PORT'] = port
        self.client.containers.run(
            name="aimmo-{}-workers-{}".format(self.game_id, self.player_id),
            image='ocadotechnology/aimmo-game-workers:test',
            ports={f"{port}/tcp": port},
            **template)
        worker_url = 'http://%s:%d' % (
            self.host,
            port,
        )
        LOGGER.info("Worker started for %s, listening at %s", self.player_id, worker_url)
        return worker_url

    def remove_worker(self, player_id):
        self.kill()
