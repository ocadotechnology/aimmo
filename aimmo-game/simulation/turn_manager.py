import logging
import requests
import time
from Queue import PriorityQueue
from threading import Lock
from threading import Thread

from simulation.action import PRIORITIES

LOGGER = logging.getLogger(__name__)


class GameStateProvider:
    """
    Thread-safe container for the world state.

    TODO: think about changing to snapshot rather than lock?
    """

    def __init__(self):
        self._game_state = None
        self._lock = Lock()

    def __enter__(self):
        self._lock.acquire()
        return self._game_state

    def __exit__(self, type, value, traceback):
        self._lock.release()

    def set_world(self, new_game_state):
        self._lock.acquire()
        self._game_state = new_game_state
        self._lock.release()


state_provider = GameStateProvider()


class TurnManager(Thread):
    """
    Game loop
    """
    daemon = True

    def __init__(self, game_state, end_turn_callback, concurrent_turns=True):
        state_provider.set_world(game_state)
        self.end_turn_callback = end_turn_callback
        self.concurrent_turns = concurrent_turns
        super(TurnManager, self).__init__()

    def run_sequential_turn(self):
        '''
        Get and apply each avatar's action in turn.
        '''
        with state_provider as game_state:
            avatars = game_state.avatar_manager.active_avatars

        for avatar in avatars:
            self._register_action(avatar)
            with state_provider as game_state:
                if avatar.action.is_legal(game_state.world_map):
                    avatar.action.apply(game_state.world_map)
                else:
                    avatar.action.reject()
                game_state.world_map.clear_cell_actions(avatar.action.target_location)
                avatar.clear_action()

    def run_concurrent_turn(self):
        '''
        Concurrently get the intended actions from all avatars and register
        them on the world map. Then apply actions in order of priority.
        '''
        with state_provider as game_state:
            avatars = game_state.avatar_manager.active_avatars

        threads = [Thread(target=self._register_action,
                          args=(avatar,)) for avatar in avatars]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        # Waits applied first, then attacks, then moves.
        avatars.sort(key=lambda a: PRIORITIES[type(a.action)])

        for action in (a.action for a in avatars if a.action is not None):
            with state_provider as game_state:
                if action.is_legal(game_state.world_map):
                    try:
                        action.chain(game_state.world_map, action)
                    except AttributeError:
                        action.apply(game_state.world_map)
                else:
                    action.reject()

        for avatar in avatars:
            with state_provider as game_state:
                game_state.world_map.clear_cell_actions(avatar.action.target_location)
                avatar.clear_action()

    def _register_action(self, avatar):
        '''
        Send an avatar its view of the game state and register its chosen action.
        '''
        with state_provider as game_state:
            state_view = game_state.get_state_for(avatar)

        if avatar.decide_action(state_view):
            with state_provider as game_state:
                avatar.action.register(game_state.world_map)

    def run(self):
        while True:
            if self.concurrent_turns:
                self.run_concurrent_turn()
            else:
                self.run_sequential_turn()

            with state_provider as game_state:
                game_state.update_environment()
                game_state.world_map.apply_score()

            self.end_turn_callback()
            time.sleep(0.5)
