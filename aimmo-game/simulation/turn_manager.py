import logging
import requests
import threading
import time
from threading import Lock
from simulation.action import ACTIONS

LOGGER = logging.getLogger(__name__)


class WorldStateProvider:
    """
    Thread-safe container for the world state.

    TODO: think about changing to snapshot rather than lock?
    """

    def __init__(self):
        self._world_state = None
        self._lock = Lock()

    def lock_and_get_world(self):
        self._lock.acquire()
        return self._world_state

    def release_lock(self):
        self._lock.release()

    def set_world(self, new_world_state):
        self._lock.acquire()
        self._world_state = new_world_state
        self._lock.release()

world_state_provider = WorldStateProvider()


class TurnManager(threading.Thread):
    """
    Game loop
    """
    daemon = True

    def __init__(self, game_state, end_turn_callback):
        world_state_provider.set_world(game_state)
        self.end_turn_callback = end_turn_callback
        super(TurnManager, self).__init__()

    def _update_environment(self, game_state):
        num_avatars = len(game_state.avatar_manager.active_avatars)
        game_state.world_map.reconstruct_interactive_state(num_avatars)

    def run_turn(self):
        try:
            game_state = world_state_provider.lock_and_get_world()

            for avatar in game_state.avatar_manager.active_avatars:
                turn_state = game_state.get_state_for(avatar)
                try:
                    data = requests.post(avatar.worker_url, json=turn_state).json()
                except ValueError as err:
                    LOGGER.info("Failed to get turn result: %s", err)
                else:
                    try:
                        action_data = data['action']
                        action_class = ACTIONS[action_data['action_type']]
                        action = action_class(**action_data.get('options', {}))
                    except (KeyError, ValueError) as err:
                        LOGGER.info("Bad action data supplied: %s", err)
                    else:
                        action.apply(game_state, avatar)

            self._update_environment(game_state)

        finally:
            world_state_provider.release_lock()

    def run(self):
        while True:
            self.run_turn()
            self.end_turn_callback()
            time.sleep(0.5)
