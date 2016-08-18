import logging
import requests
import time
from Queue import PriorityQueue
from threading import Lock
from threading import Thread

from simulation.action import PRIORITIES

LOGGER = logging.getLogger(__name__)


class TurnManager(Thread):
    """
    Game loop
    """
    daemon = True

    def __init__(self, game_state, end_turn_callback):
        self.game_state = game_state
        self.end_turn_callback = end_turn_callback
        super(TurnManager, self).__init__()

    def run_turn(self):
        raise NotImplementedError("Abstract method.")

    def _register_action(self, avatar):
        '''
        Send an avatar its view of the game state and register its chosen action.
        '''
        with self.game_state as game_state:
            state_view = game_state.get_state_for(avatar)

        if avatar.decide_action(state_view):
            with self.game_state as game_state:
                avatar.action.register(game_state.world_map)

    def run(self):
        while True:
            self.run_turn()

            with self.game_state as game_state:
                game_state.update_environment()
                game_state.world_map.apply_score()

            self.end_turn_callback()
            time.sleep(0.5)


class SequentialTurnManager(TurnManager):
    def run_turn(self):
        '''
        Get and apply each avatar's action in turn.
        '''
        with self.game_state as game_state:
            avatars = game_state.avatar_manager.active_avatars

        for avatar in avatars:
            self._register_action(avatar)
            with self.game_state as game_state:
                location_to_clear = avatar.action.target_location
                avatar.action.process(game_state.world_map)
                game_state.world_map.clear_cell_actions(location_to_clear)


class ConcurrentTurnManager(TurnManager):
    def run_turn(self):
        '''
        Concurrently get the intended actions from all avatars and register
        them on the world map. Then apply actions in order of priority.
        '''
        with self.game_state as game_state:
            avatars = game_state.avatar_manager.active_avatars

        threads = [Thread(target=self._register_action,
                          args=(avatar,)) for avatar in avatars]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        # Waits applied first, then attacks, then moves.
        avatars.sort(key=lambda a: PRIORITIES[type(a.action)])

        locations_to_clear = {a.action.target_location for a in avatars
                              if a.action is not None}

        for action in (a.action for a in avatars if a.action is not None):
            with self.game_state as game_state:
                action.process(game_state.world_map)

        for location in locations_to_clear:
            with self.game_state as game_state:
                game_state.world_map.clear_cell_actions(location)


TURN_MANAGERS = {
    'sequential': SequentialTurnManager,
    'concurrent': ConcurrentTurnManager,
}
