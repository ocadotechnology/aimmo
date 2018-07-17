import atexit
import itertools
import json
import logging
import os
import subprocess
import tempfile
import requests

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
        env = os.environ.copy()
        data_dir = tempfile.mkdtemp()

        LOGGER.debug('Data dir is %s', data_dir)
        data = requests.get("http://127.0.0.1:{}/player/{}".format(self.port, player_id)).json()

        options = data['options']
        with open('{}/options.json'.format(data_dir), 'w') as options_file:
            json.dump(options, options_file)

        code = data['code']
        with open('{}/avatar.py'.format(data_dir), 'w') as avatar_file:
            avatar_file.write(code)

        env['PYTHONPATH'] = data_dir

        process = subprocess.Popen(['python', 'service.py', self.host, str(port), str(data_dir)],
                                   cwd=self.worker_directory, env=env)
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
