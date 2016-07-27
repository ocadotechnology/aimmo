import logging
import requests
import threading
import time
from threading import Lock
from threading import Thread
from simulation.action import ACTIONS

LOGGER = logging.getLogger(__name__)


class GameStateProvider:
    """
    Thread-safe container for the world state.

    TODO: think about changing to snapshot rather than lock?
    """

    def __init__(self):
        self._world_state = None
        self._lock = Lock()

    def __enter__(self):
        self._lock.acquire()
        return self._world_state

    def __exit__(self, type, value, traceback):
        self._lock.release()

    def set_world(self, new_world_state):
        self._lock.acquire()
        self._world_state = new_world_state
        self._lock.release()


game_state_provider = GameStateProvider()


class TurnManager(threading.Thread):
    """
    Game loop
    """
    daemon = True

    def __init__(self, game_state, end_turn_callback):
        game_state_provider.set_world(game_state)
        self.end_turn_callback = end_turn_callback
        super(TurnManager, self).__init__()

    def _update_environment(self, game_state):
        num_avatars = len(game_state.avatar_manager.active_avatars)
        game_state.world_map.reconstruct_interactive_state(num_avatars)

    def run_turn(self):
        with game_state_provider as game_state:
            active_avatars = game_state.avatar_manager.active_avatars

        for avatar in active_avatars:
            action = self._get_action(avatar)
            with game_state_provider as game_state:
                action.apply(game_state)

        with game_state_provider as game_state:
            self._update_environment(game_state)

    def get_actions(self):
        '''
        Concurrently get the intended actions from all avatars, and register
        them with the game state.
        '''
        raise NotImplementedError()

    def _get_action(self, avatar):
        '''
        Send an avatar its view of the game state and return its chosen action.
        '''
        with game_state_provider as game_state:
            state_view = game_state.get_state_for(avatar)

        try:
            data = requests.post(avatar.worker_url, json=state_view).json()
        except ValueError as err:
            LOGGER.info('Failed to get turn result: %s', err)
        else:
            try:
                action_data = data['action']
                action_type = action_data['action_type']
                action = ACTIONS[action_type](**action_data.get('options', {}))
            except (KeyError, ValueError) as err:
                LOGGER.info('Bad action data supplied: %s', err)
            else:
                action.avatar = avatar
                return action

    def run(self):
        while True:
            self.run_turn()
            self.end_turn_callback()
            time.sleep(0.5)
