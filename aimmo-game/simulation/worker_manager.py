import logging
import os
import subprocess
import threading
import time
from eventlet.greenpool import GreenPool
from eventlet.semaphore import Semaphore

import requests
from pykube import HTTPClient
from pykube import KubeConfig
from pykube import Pod

LOGGER = logging.getLogger(__name__)


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

    def remove_user_if_code_is_different(self, user):
        with self._lock:
            existing_code = self._user_codes.get(user['id'], None)
            if existing_code != user['code']:
                # Remove avatar from the game, so it stops being called for turns
                if existing_code is not None:
                    self._remove_avatar(user['id'])
                return True
            else:
                return False

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


class WorkerManager(threading.Thread):
    """
    Methods of this class must be thread safe unless explicitly stated.
    """
    daemon = True

    def __init__(self, game_state, users_url):
        """

        :param thread_pool:
        """
        self._data = _WorkerManagerData(game_state, {})
        self.users_url = users_url
        self._pool = GreenPool(size=3)
        super(WorkerManager, self).__init__()

    def get_code(self, player_id):
        return self._data.get_code(player_id)

    def get_persistent_state(self, player_id):
        """Get the persistent state for a worker."""

        return None

    def create_worker(self, player_id):
        """Create a worker."""

        raise NotImplemented

    def remove_worker(self, player_id):
        """Remove a worker for the given player."""

        raise NotImplemented

    # TODO handle failure
    def spawn(self, user):
        # Get persistent state from worker
        persistent_state = self.get_persistent_state(user['id'])

        # Kill worker
        LOGGER.info("Removing worker for user %s" % user['id'])
        self.remove_worker(user['id'])

        self._data.set_code(user)

        # Spawn worker
        LOGGER.info("Spawning worker for user %s" % user['id'])
        worker_url = self.create_worker(user['id'])

        # Add avatar back into game
        self._data.add_avatar(user, worker_url)

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
            users_to_add = []
            for user in game['users']:
                if self._data.remove_user_if_code_is_different(user):
                    users_to_add.append(user)
            LOGGER.debug("Need to add users: %s" % [x['id'] for x in users_to_add])

            # Add missing users
            self._parallel_map(self.spawn, users_to_add)

            # Delete extra users
            known_avatars = set(user['id'] for user in game['users'])
            removed_user_ids = self._data.remove_unknown_avatars(known_avatars)
            LOGGER.debug("Removing users: %s" % removed_user_ids)
            self._parallel_map(self.remove_worker, removed_user_ids)

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
    worker_path = os.path.join(worker_directory, 'run.sh')

    def __init__(self, *args, **kwargs):
        self.workers = {}
        self.next_port = 1989
        super(LocalWorkerManager, self).__init__(*args, **kwargs)

    def create_worker(self, player_id):
        assert(player_id not in self.workers)
        self.next_port += 1
        process_args = [
            'bash',
            self.worker_path,
            self.host,
            str(self.next_port),
        ]
        env = os.environ.copy()
        env['DATA_URL'] = "http://127.0.0.1:5000/player/%d" % player_id
        self.workers[player_id] = subprocess.Popen(process_args, cwd=self.worker_directory, env=env)
        worker_url = 'http://%s:%d' % (
            self.host,
            self.next_port,
        )
        LOGGER.info("Worker started for %s, listening at %s", player_id, worker_url)
        time.sleep(5)
        return worker_url

    def remove_worker(self, player_id):
        if player_id in self.workers:
            self.workers[player_id].kill()
            del self.workers[player_id]


class KubernetesWorkerManager(WorkerManager):
    '''Kubernetes worker manager.'''

    def __init__(self, *args, **kwargs):
        self.api = HTTPClient(KubeConfig.from_service_account())
        self.game_name = os.environ['GAME_NAME']
        self.game_url = os.environ['GAME_URL']
        super(KubernetesWorkerManager, self).__init__(*args, **kwargs)

    def create_worker(self, player_id):
        pod = Pod(
            self.api,
            {
             'kind': 'Pod',
             'apiVersion': 'v1',
             'metadata': {
                'generateName': "aimmo-%s-worker-%s-" % (self.game_name, player_id),
                'labels': {
                    'app': 'aimmo-game-worker',
                    'game': self.game_name,
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
                        'image': 'ocadotechnology/aimmo-game-worker:latest',
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
                        },
                    },
                ],
             },
            }
        )
        pod.create()
        time.sleep(20)
        pod.reload()
        worker_url = "http://%s:5000" % pod.obj['status']['podIP']
        LOGGER.info("Worker started for %s, listening at %s", player_id, worker_url)
        return worker_url

    def remove_worker(self, player_id):
        for pod in Pod.objects(self.api).filter(selector={
            'app': 'aimmo-game-worker',
            'game': self.game_name,
            'player': str(player_id),
        }):
            pod.delete()

WORKER_MANAGERS = {
    'local': LocalWorkerManager,
    'kubernetes': KubernetesWorkerManager,
}
