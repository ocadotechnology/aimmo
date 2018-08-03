from threading import RLock


class GameStateProvider(object):
    """
    Thread-safe container for the world state.

    """

    def __init__(self):
        self._game_state = None
        self._lock = RLock()

    def __enter__(self):
        self._lock.acquire()
        return self._game_state

    def __exit__(self, type, value, traceback):
        self._lock.release()

    def set_world(self, new_game_state):
        self._lock.acquire()
        self._game_state = new_game_state
        self._lock.release()
