import atexit
import itertools
import logging
import os
import subprocess
import docker
import json

from .worker_manager import WorkerManager

LOGGER = logging.getLogger(__name__)


class LocalWorkerManager(WorkerManager):
    """Relies on them already being created already."""

    host = os.environ.get('LOCALHOST_IP', '127.0.0.1')
    worker_directory = os.path.join(
        os.path.dirname(__file__),
        '../../../aimmo-game-worker/',
    )

    def __init__(self, *args, **kwargs):
        self.workers = {}
        self.game_id = os.environ['GAME_ID']
        self.port_counter = itertools.count(1989 + int(self.game_id) * 10000)
        self.client = docker.from_env()
        super(LocalWorkerManager, self).__init__(*args, **kwargs)

    def create_worker(self, player_id):
        assert(player_id not in self.workers)
        port = next(self.port_counter)

        template_string = os.environ.get('CONTAINER_TEMPLATE')
        if template_string:
            template = json.loads(template_string)
        else:
            template = {
                'environment': {}
            }
        data_url = 'http://{}:{}/player/{}'.format(self.host, self.port, player_id)
        template['environment']['DATA_URL'] = data_url
        template['environment']['PORT'] = port
        container = self.client.containers.run(
            name="aimmo-{}-worker-{}".format(self.game_id, player_id),
            image='ocadotechnology/aimmo-game-worker:test',
            ports={f"{port}/tcp": port},
            **template)
        self.workers[player_id] = container
        worker_url = 'http://%s:%d' % (
            self.host,
            port,
        )
        LOGGER.info("Worker started for %s, listening at %s", player_id, worker_url)
        return worker_url

    def remove_worker(self, player_id):
        if player_id in self.workers:
            self.workers[player_id].kill()
            del self.workers[player_id]
