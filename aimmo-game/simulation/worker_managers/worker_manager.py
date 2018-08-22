import logging
import threading
import time

import requests
from eventlet.greenpool import GreenPool
from eventlet.semaphore import Semaphore

LOGGER = logging.getLogger(__name__)


class _WorkerManagerData(object):
    """
    This class is thread safe
    """

    def __init__(self, user_codes):
        self._user_codes = user_codes
        self._lock = Semaphore()

    def set_code(self, user):
        with self._lock:
            self._user_codes[user['id']] = user['code']

    def get_code(self, player_id):
        with self._lock:
            return self._user_codes[player_id]


class WorkerManager(object):
    """
    Methods of this class must be thread safe unless explicitly stated.
    """
    def __init__(self, port):
        self._data = _WorkerManagerData({})
        self._pool = GreenPool(size=3)
        self.avatar_id_to_worker = {}
        self.port = port
        super(WorkerManager, self).__init__()

    def get_code(self, player_id):
        return self._data.get_code(player_id)

    def create_worker(self, player_id):
        raise NotImplementedError

    def remove_worker(self, player_id):
        # TODO: Remove worker dummy object
        raise NotImplementedError

    def update_code(self, user):
        self._data.set_code(user)

    def add_new_user(self, user_id):
        worker_url = self.create_worker(user_id)
        self.avatar_id_to_worker = {user_id: 'WorkerDummyObject'}
        print('Worker url: {}'.format(worker_url))
        return user_id, worker_url

    def _parallel_map(self, func, iterable_args):
        return list(self._pool.imap(func, iterable_args))

    def add_workers(self, users_to_add):
        return dict(self._parallel_map(self.add_new_user, users_to_add))

    def delete_workers(self, users_to_delete):
        self._parallel_map(self.remove_worker, users_to_delete)

    def update_worker_codes(self, users):
        self._parallel_map(self.update_code, users)
