import logging
import requests
import time
from Queue import PriorityQueue
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


game_state_provider = GameStateProvider()


class TurnManager(Thread):
    """
    Game loop
    """
    daemon = True

    def __init__(self, game_state, end_turn_callback, concurrent_turns=True):
        game_state_provider.set_world(game_state)
        self.end_turn_callback = end_turn_callback
        self.concurrent_turns = concurrent_turns
        super(TurnManager, self).__init__()

    def run_sequential_turn(self):
        '''
        Get and apply each avatar's action in turn.
        '''
        with game_state_provider as game_state:
            avatars = game_state.avatar_manager.active_avatars

        action_queue = PriorityQueue()

        for avatar in avatars:
            self._register_action(avatar, action_queue)
            action = action_queue.get()[1]
            with game_state_provider as game_state:
                if action.is_legal(game_state.world_map):
                    action.apply(game_state.world_map)
                else:
                    action.reject()
                game_state.world_map.clear_cell_actions(action.target_location)

    def run_concurrent_turn(self):
        '''
        Concurrently get the intended actions from all avatars and register
        them on the world map. Then apply actions in order of priority.
        '''
        with game_state_provider as game_state:
            avatars = game_state.avatar_manager.active_avatars

        action_queue = PriorityQueue()
        threads = [Thread(target=self._register_action,
                          args=(avatar, action_queue)) for avatar in avatars]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        cells_to_clear = set()

        while not action_queue.empty():
            action = action_queue.get()[1]
            with game_state_provider as game_state:
                if action.is_legal(game_state.world_map):
                    action.apply(game_state.world_map)
                else:
                    action.reject()
            cells_to_clear.add(action.target_location)

        for cell in cells_to_clear:
            with game_state_provider as game_state:
                game_state.world_map.clear_cell_actions(cell)

    def _register_action(self, avatar, action_queue):
        '''
        Send an avatar its view of the game state and register its chosen action.
        '''
        with game_state_provider as game_state:
            state_view = game_state.get_state_for(avatar)

        if avatar.decide_action(state_view):
            with game_state_provider as game_state:
                avatar.action.target(game_state.world_map)
            action_queue.put((avatar.action.priority, avatar.action))

    def run(self):
        while True:
            if self.concurrent_turns:
                self.run_concurrent_turn()
            else:
                self.run_sequential_turn()

            with game_state_provider as game_state:
                game_state.update_environment()
                game_state.world_map.apply_score()

            self.end_turn_callback()
            time.sleep(0.5)
