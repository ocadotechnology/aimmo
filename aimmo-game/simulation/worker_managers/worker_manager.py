import logging

from eventlet.greenpool import GreenPool
from eventlet.semaphore import Semaphore

LOGGER = logging.getLogger(__name__)


class _WorkerManagerData(object):
    """
    This class is thread safe
    """

    def __init__(self, user_codes):
        self._user_codes = user_codes

    def set_code(self, player):
        self._user_codes[player['id']] = player['code']

    def get_code(self, player_id):
        return self._user_codes[player_id]


class WorkerManager(object):
    """
    Methods of this class must be thread safe unless explicitly stated.
    """
    def __init__(self, port=5000):
        self._data = _WorkerManagerData({})
        self._pool = GreenPool(size=3)
        self.avatar_id_to_worker = {}
        self.port = port

    def get_code(self, player_id):
        return self._data.get_code(player_id)

    def create_worker(self, player_id):
        raise NotImplementedError

    def remove_worker(self, player_id):
        raise NotImplementedError

    def update_code(self, player):
        self._data.set_code(player)

    def add_new_worker(self, player_id):
        worker_url = self.create_worker(player_id)
        self.avatar_id_to_worker[player_id] = 'WorkerDummyObject'
        print('Worker url: {}'.format(worker_url))
        return player_id, worker_url

    def _parallel_map(self, func, iterable_args):
        return list(self._pool.imap(func, iterable_args))

    def add_workers(self, users_to_add):
        return dict(self._parallel_map(self.add_new_worker, users_to_add))

    def delete_workers(self, players_to_delete):
        print('Users to delete: {}'.format(players_to_delete))
        self._parallel_map(self.delete_worker, players_to_delete)

    def delete_worker(self, player):
        del self.avatar_id_to_worker[player]
        self.remove_worker(player)

    def update_worker_codes(self, players):
        self._parallel_map(self.update_code, players)
