import atexit
import itertools
import logging
import os
import subprocess

from .worker_manager import WorkerManager

LOGGER = logging.getLogger(__name__)


class LocalWorkerManager(WorkerManager):
    """Relies on them already being created already."""

    host = '127.0.0.1'
    worker_directory = os.path.join(
        os.path.dirname(__file__),
        '../../../aimmo-game-worker/',
    )

    def __init__(self, *args, **kwargs):
        self.workers = {}
        self.port_counter = itertools.count(1989)
        super(LocalWorkerManager, self).__init__(*args, **kwargs)

    def create_worker(self, player_id):
        assert(player_id not in self.workers)
        port = self.port_counter.next()

        data_url = 'http://{}:{}/player/{}'.format(self.host, self.port, player_id)

        process = subprocess.Popen(['python', 'service.py', self.host, str(port), data_url],
                                   cwd=self.worker_directory)
        atexit.register(process.kill)
        self.workers[player_id] = process
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
