import atexit
import itertools
import json
import logging
import os
import subprocess
import tempfile
import threading
import time

import requests
from eventlet.greenpool import GreenPool
from eventlet.semaphore import Semaphore
from pykube import HTTPClient
from pykube import KubeConfig
from pykube import Pod

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class _WorkerManagerData(object):
    """
    This class is thread safe
    """

    def __init__(self, game_state, user_codes):
        self._game_state = game_state
        self._user_codes = user_codes
        self._lock = Semaphore()

    def _remove_avatar(self, user_id):
        assert self._lock.locked
        self._game_state.remove_avatar(user_id)
        del self._user_codes[user_id]

    def is_new_avatar(self, user):
        with self._lock:
            existing_code = self._user_codes.get(user['id'], None)
            return existing_code is None

    def remove_user_if_code_is_different(self, user):
        with self._lock:
            existing_code = self._user_codes.get(user['id'], None)
            return existing_code != user['code']

    def add_avatar(self, user, worker_url):
        with self._lock:
            # Add avatar back into game
            self._game_state.add_avatar(
                user_id=user['id'], worker_url="%s/turn/" % worker_url)

    def set_code(self, user):
        with self._lock:
            self._user_codes[user['id']] = user['code']

    def get_code(self, player_id):
        with self._lock:
            return self._user_codes[player_id]

    def remove_unknown_avatars(self, known_user_ids):
        with self._lock:
            unknown_user_ids = set(self._user_codes) - frozenset(known_user_ids)
            for u in unknown_user_ids:
                self._remove_avatar(u)
            return unknown_user_ids

    def set_main_avatar(self, avatar_id):
        with self._lock:
            self._game_state.main_avatar_id = avatar_id


class WorkerManager(threading.Thread):
    """
    Methods of this class must be thread safe unless explicitly stated.
    """
    daemon = True

    def __init__(self, game_state, users_url, port=5000):
        """

        :param thread_pool:
        """
        self._data = _WorkerManagerData(game_state, {})
        self.users_url = users_url
        self._pool = GreenPool(size=3)
        self.port = port
        super(WorkerManager, self).__init__()

    def get_code(self, player_id):
        return self._data.get_code(player_id)

    def create_worker(self, player_id):
        """Create a worker."""

        raise NotImplemented

    def remove_worker(self, player_id):
        """Remove a worker for the given player."""

        raise NotImplemented

    def recreate_worker(self, user):
        """
        Helper function to kill the worker, set new code in the WorkerManagerData
        and spawn a new worker.
        :param user_id:
        :return:
        """
        user_id = user['id']

        LOGGER.info("Removing worker for user %s" % user_id)
        self.remove_worker(user_id)

        self._data.set_code(user)

        # Spawn worker
        LOGGER.info("Spawning worker for user %s" % user_id)
        worker_url = self.create_worker(user_id)

        return worker_url

    def recreate_user(self, user):
        """
        Removes and creates new worker pods. Sets the new user code in between
        to the user_codes of _WorkerManagerData.
        :param user: Dict containing the user code, id etc.
        """
        user_id = user['id']

        worker_url = self.recreate_worker(user)

        # Update the worker_url of the avatar.
        # TODO: refactor this so that you don't need to use these private instance variables
        avatar = self._data._game_state.avatar_manager.get_avatar(user_id)

        LOGGER.info("worker_url " + "%s/turn/" % worker_url)
        avatar.worker_url = "%s/turn/" % worker_url

    def add_new_user(self, user):
        """
        TODO
        :param user: Dict containing the user code, id etc.
        """
        user_id = user['id']

        worker_url = self.recreate_worker(user)

        # Add avatar into game
        self._data.add_avatar(user, worker_url)
        LOGGER.info('Added user %s', user_id)

    def _parallel_map(self, func, iterable_args):
        list(self._pool.imap(func, iterable_args))

    def update(self):
        try:
            LOGGER.info("Waking up")
            game_data = requests.get(self.users_url).json()
        except (requests.RequestException, ValueError) as err:
            LOGGER.error("Failed to obtain game data : %s", err)
        else:
            game = game_data['main']

            # Remove users with different code
            users_to_recreate = []
            new_users_to_add = []

            for user in game['users']:
                if self._data.is_new_avatar(user):
                    new_users_to_add.append(user)
                if self._data.remove_user_if_code_is_different(user):
                    users_to_recreate.append(user)
            LOGGER.debug("Need to add users: %s" % [x['id'] for x in new_users_to_add])

            # Add new worker pods
            self._parallel_map(self.add_new_user, new_users_to_add)

            # Recreate worker pods
            self._parallel_map(self.recreate_user, users_to_recreate)


        # Delete extra users
            known_avatars = set(user['id'] for user in game['users'])
            removed_user_ids = self._data.remove_unknown_avatars(known_avatars)
            LOGGER.debug("Removing users: %s" % removed_user_ids)
            self._parallel_map(self.remove_worker, removed_user_ids)

            # Update main avatar
            self._data.set_main_avatar(game_data['main']['main_avatar'])

    def run(self):
        while True:
            self.update()
            LOGGER.info("Sleeping")
            time.sleep(10)


class LocalWorkerManager(WorkerManager):
    """Relies on them already being created already."""

    host = '127.0.0.1'
    worker_directory = os.path.join(
        os.path.dirname(__file__),
        '../../aimmo-game-worker/',
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

        process = subprocess.Popen(['python', 'service.py', self.host, str(port), str(data_dir)], cwd=self.worker_directory, env=env)
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


class KubernetesWorkerManager(WorkerManager):
    """Kubernetes worker manager."""

    def __init__(self, *args, **kwargs):
        self.api = HTTPClient(KubeConfig.from_service_account())
        self.game_id = os.environ['GAME_ID']
        self.game_url = os.environ['GAME_URL']
        super(KubernetesWorkerManager, self).__init__(*args, **kwargs)

    def create_worker(self, player_id):
        pod = Pod(
            self.api,
            {
             'kind': 'Pod',
             'apiVersion': 'v1',
             'metadata': {
                'generateName': "aimmo-%s-worker-%s-" % (self.game_id, player_id),
                'labels': {
                    'app': 'aimmo-game-worker',
                    'game': self.game_id,
                    'player': str(player_id),
                    },
                },
             'spec': {
                'containers': [
                    {
                        'env': [
                            {
                                'name': 'DATA_URL',
                                'value': "%s/player/%d" % (self.game_url, player_id),
                            },
                        ],
                        'name': 'aimmo-game-worker',
                        'image': 'ocadotechnology/aimmo-game-worker:%s' % os.environ.get('IMAGE_SUFFIX', 'latest'),
                        'ports': [
                            {
                                'containerPort': 5000,
                                'protocol': 'TCP'
                            }
                        ],
                        'resources': {
                            'limits': {
                                'cpu': '10m',
                                'memory': '64Mi',
                            },
                            'requests': {
                                'cpu': '7m',
                                'memory': '32Mi',
                            },
                        },
                    },
                ],
             },
            }
        )
        pod.create()
        iterations = 0
        while pod.obj['status']['phase'] == 'Pending':
            if iterations > 30:
                raise EnvironmentError('Could not start worker %s, details %s' % (player_id, pod.obj))
            LOGGER.debug('Waiting for worker %s', player_id)
            time.sleep(5)
            pod.reload()
            iterations += 1
        worker_url = "http://%s:5000" % pod.obj['status']['podIP']
        LOGGER.info("Worker started for %s, listening at %s", player_id, worker_url)
        return worker_url

    def remove_worker(self, player_id):
        for pod in Pod.objects(self.api).filter(selector={
            'app': 'aimmo-game-worker',
            'game': self.game_id,
            'player': str(player_id),
        }):
            LOGGER.debug('Removing pod %s', pod.obj['spec'])
            pod.delete()

WORKER_MANAGERS = {
    'local': LocalWorkerManager,
    'kubernetes': KubernetesWorkerManager,
}
