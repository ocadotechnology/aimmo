import itertools
import json
import logging
import os

import docker
from docker.models.containers import Container

from .worker import Worker

LOGGER = logging.getLogger(__name__)

port_counter = itertools.count(1989 + int(os.environ.get("GAME_ID", 0)) * 10000)


class LocalWorker(Worker):
    """Relies on them already being created already."""

    host = os.environ.get("LOCALHOST_IP", "127.0.0.1")
    worker_directory = os.path.join(
        os.path.dirname(__file__), "../../../aimmo-game-worker/"
    )

    def __init__(self, *args, **kwargs):
        self.game_id = os.environ.get("GAME_ID", 0)
        self.client = docker.from_env()
        self.container: Container = None
        super(LocalWorker, self).__init__(*args, **kwargs)

    @staticmethod
    def _init_port_counter():
        global port_counter
        port_counter = itertools.count(1989 + int(os.environ["GAME_ID"]) * 10000)

    def _create_worker(self):
        global port_counter
        port = next(port_counter)
        template_string = os.environ.get("CONTAINER_TEMPLATE")
        if template_string:
            template = json.loads(template_string)
        else:
            template = {"environment": {}}
        data_url = "http://{}:{}/player/{}".format(
            self.host, self.game_port, self.player_id
        )
        template["environment"]["DATA_URL"] = data_url
        template["environment"]["PORT"] = port
        self.container = self.client.containers.run(
            name="aimmo-{}-worker-{}".format(self.game_id, self.player_id),
            image="ocadotechnology/aimmo-game-worker:test",
            ports={f"{port}/tcp": port},
            **template,
        )
        worker_url = "http://%s:%d" % (self.host, port)
        LOGGER.info(
            "Worker started for %s, listening at %s", self.player_id, worker_url
        )
        return worker_url

    def remove_worker(self):
        self.container.kill()
