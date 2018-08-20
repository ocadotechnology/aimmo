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

    def is_new_code_different_than_existing(self, user):
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

    def get_avatar_from_user_id(self, user_id):
        """
        Accesses the avatar manager from the game state to receive the avatar
        object.
        :param user_id: The ID of the worker in this game instance.
        :return: Avatar object
        """
        with self._lock:
            return self._game_state.avatar_manager.get_avatar(user_id)


class WorkerManager(threading.Thread):
    """
    Methods of this class must be thread safe unless explicitly stated.
    """
    daemon = True

    def __init__(self, game_state, communicator, port=5000):
        self._data = _WorkerManagerData(game_state, {})
        self.communicator = communicator
        self._pool = GreenPool(size=3)
        self.port = port
        super(WorkerManager, self).__init__()

    def get_code(self, player_id):
        return self._data.get_code(player_id)

    def create_worker(self, player_id):
        """Create a worker."""

        raise NotImplementedError

    def remove_worker(self, player_id):
        """Remove a worker for the given player."""

        raise NotImplementedError

    def update_code(self, user):
        """
        Updates the code for a user.
        """
        self._data.set_code(user)

    def add_new_user(self, user):
        """
        Adds a new avatar to the game state so we keep track of it in each turn.
        :param user: Dict containing the user code, id etc.
        """
        user_id = user['id']
        self._data.set_code(user)
        worker_url = self.create_worker(user_id)

        # Add avatar into game
        self._data.add_avatar(user, worker_url)
        LOGGER.info('Added user %s', user_id)

    def _parallel_map(self, func, iterable_args):
        list(self._pool.imap(func, iterable_args))

    def update(self):
        try:
            LOGGER.info("Waking up")
            game_data = self.communicator.get_game_metadata()
        except (requests.RequestException, ValueError) as err:
            LOGGER.error("Failed to obtain game data : %s", err)
        else:
            game = game_data['main']

            # Update users with different code
            users_to_update = []
            new_users_to_add = []

            for user in game['users']:
                if self._data.is_new_avatar(user):
                    new_users_to_add.append(user)
                if self._data.is_new_code_different_than_existing(user):
                    users_to_update.append(user)
            LOGGER.debug("Need to add users: %s" % [x['id'] for x in new_users_to_add])

            # Add new worker pods
            self._parallel_map(self.add_new_user, new_users_to_add)

            # Update code
            self._parallel_map(self.update_code, users_to_update)

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
