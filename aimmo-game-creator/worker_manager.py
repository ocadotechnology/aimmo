import logging
import os
import subprocess
import time
from abc import ABCMeta, abstractmethod

import pykube
import requests
from eventlet.greenpool import GreenPool
from eventlet.semaphore import Semaphore

LOGGER = logging.getLogger(__name__)


class _WorkerManagerData(object):
    """
    This class is thread safe
    """

    def __init__(self):
        self._games = set()
        self._lock = Semaphore()

    def _remove_game(self, game_id):
        assert self._lock.locked
        self._games.remove(game_id)

    def _add_game(self, game_id):
        assert self._lock.locked
        self._games.add(game_id)

    def remove_unknown_games(self, known_games):
        with self._lock:
            unknown_games = self._games - frozenset(known_games)
            for u in unknown_games:
                self._remove_game(u)
            return unknown_games

    def get_games(self):
        with self._lock:
            for g in self._games:
                yield g

    def add_new_games(self, all_games):
        with self._lock:
            new_games = frozenset(all_games) - self._games
            for n in new_games:
                self._add_game(n)
            return new_games


class WorkerManager(object):
    """
    Methods of this class must be thread safe unless explicitly stated.
    """
    __metaclass__ = ABCMeta
    daemon = True

    def __init__(self, games_url):
        """

        :param thread_pool:
        """
        self._data = _WorkerManagerData()
        self.games_url = games_url
        self._pool = GreenPool(size=3)
        super(WorkerManager, self).__init__()

    def get_persistent_state(self, player_id):
        """Get the persistent state for a worker."""

        return None

    @abstractmethod
    def create_worker(self, player_id):
        """Create a worker."""

        raise NotImplemented

    @abstractmethod
    def remove_worker(self, player_id):
        """Remove a worker for the given player."""

        raise NotImplemented

    # TODO handle failure
    def spawn(self, game_id, game_data):
        # Kill worker
        LOGGER.info("Removing worker for game %s" % game_data['name'])
        self.remove_worker(game_id)

        # Spawn worker
        LOGGER.info("Spawning worker for game %s" % game_data['name'])
        game_data['GAME_API_URL'] = '{}{}/'.format(self.games_url, game_id)
        self.create_worker(game_id, game_data)

    def _parallel_map(self, func, *iterable_args):
        list(self._pool.imap(func, *iterable_args))

    def run(self):
        while True:
            self.update()
            LOGGER.info("Sleeping")
            time.sleep(10)

    def update(self):
        try:
            LOGGER.info("Waking up")
            games = requests.get(self.games_url).json()
        except (requests.RequestException, ValueError) as err:
            LOGGER.error("Failed to obtain game data : %s", err)
        else:
            games_to_add = {id: games[id]
                            for id in self._data.add_new_games(games.keys())}
            LOGGER.debug("Need to add games: %s" % games_to_add)

            # Add missing games
            self._parallel_map(self.spawn, games_to_add.keys(), games_to_add.values())

            # Delete extra games
            known_games = set(games.keys())
            removed_user_ids = self._data.remove_unknown_games(known_games)
            LOGGER.debug("Removing users: %s" % removed_user_ids)
            self._parallel_map(self.remove_worker, removed_user_ids)


class LocalWorkerManager(WorkerManager):
    """Relies on them already being created already."""

    host = '0.0.0.0'
    worker_directory = os.path.join(
        os.path.dirname(__file__),
        '../aimmo-game/',
    )
    worker_path = os.path.join(worker_directory, 'service.py')

    def __init__(self, *args, **kwargs):
        self.workers = {}
        super(LocalWorkerManager, self).__init__(*args, **kwargs)

    def create_worker(self, game_id, game_data):
        assert(game_id not in self.workers)
        port = str(6001 + int(game_id) * 1000)
        process_args = [
            'python',
            self.worker_path,
            self.host,
            port,
        ]
        env = os.environ.copy()
        game_data = {str(k):str(v) for k,v in game_data.items()}
        env.update(game_data)
        self.workers[game_id] = subprocess.Popen(process_args, cwd=self.worker_directory, env=env)
        worker_url = 'http://%s:%s' % (
            self.host,
            port,
        )
        LOGGER.info("Worker started for game %s, listening at %s", game_id, worker_url)

    def remove_worker(self, game_id):
        if game_id in self.workers:
            self.workers[game_id].kill()
            del self.workers[game_id]


class KubernetesWorkerManager(WorkerManager):
    '''Kubernetes worker manager.'''

    def __init__(self, *args, **kwargs):
        self._api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())
        super(KubernetesWorkerManager, self).__init__(*args, **kwargs)

    def _create_game_rc(self, id, environment_variables):
        environment_variables['SOCKETIO_RESOURCE'] = "game/%s/socket.io" % id
        environment_variables['GAME_ID'] = id
        environment_variables['GAME_URL'] = "http://game-%s" % id
        environment_variables['PYKUBE_KUBERNETES_SERVICE_HOST'] = 'kubernetes'
        environment_variables['IMAGE_SUFFIX'] = os.environ.get('IMAGE_SUFFIX', 'latest')
        rc = pykube.ReplicationController(
            self._api,
            {
                'kind': 'ReplicationController',
                'apiVersion': 'v1',
                'metadata': {
                    'name': "game-%s" % id,
                    'namespace': 'default',
                    'labels': {
                        'app': 'aimmo-game',
                        'game_id': id,
                    },
                },
                'spec': {
                    'replicas': 1,
                    'selector': {
                        'app': 'aimmo-game',
                        'game_id': id,
                    },
                    'template': {
                        'metadata': {
                            'labels': {
                                'app': 'aimmo-game',
                                'game_id': id,
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
                                    'image': 'ocadotechnology/aimmo-game:%s' % os.environ.get('IMAGE_SUFFIX', 'latest'),
                                    'ports': [
                                        {
                                            'containerPort': 5000,
                                        },
                                    ],
                                    'name': 'aimmo-game',
                                    'resources': {
                                        'limits': {
                                            'cpu': '1000m',
                                            'memory': '128Mi',
                                        },
                                        'requests': {
                                            'cpu': '100m',
                                            'memory': '64Mi',
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            },
        )
        rc.create()

    def _create_game_service(self, id, _config):
        service = pykube.Service(
            self._api,
            {
                'kind': 'Service',
                'apiVersion': 'v1',
                'metadata': {
                    'name': "game-%s" % id,
                    'labels': {
                        'app': 'aimmo-game',
                        'game_id': id,
                    },
                },
                'spec': {
                    'selector': {
                        'app': 'aimmo-game',
                        'game_id': id,
                    },
                    'ports': [
                        {
                            'protocol': 'TCP',
                            'port': 80,
                            'targetPort': 5000,
                        },
                    ],
                    'type': 'NodePort',
                },
            },
        )
        service.create()

    def remove_worker(self, game_id):
        for object_type in (pykube.ReplicationController, pykube.Service):
            for game in object_type.objects(self._api).\
                filter(selector={'app': 'aimmo-game',
                                 'game_id': game_id}):
                LOGGER.info('Removing %s: %s', object_type.__name__, game.name)
                game.delete()

    def create_worker(self, id, data):
        try:
            self._create_game_service(id, data)
        except pykube.exceptions.HTTPError as err:
            if 'already exists' in err.message:
                LOGGER.warning('Service for game %s already existed', id)
            else:
                raise
        self._create_game_rc(id, data)
        LOGGER.info("Worker started for %s", id)


WORKER_MANAGERS = {
    'local': LocalWorkerManager,
    'kubernetes': KubernetesWorkerManager,
}
