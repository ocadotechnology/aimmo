import time
from threading import Lock
from simulation import world_map


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


class TurnManager(object):
    """
    Game loop
    """

    def __init__(self, game_state):
        world_state_provider.set_world(game_state)

    def _update_environment(self, game_state):
        num_avatars = len(game_state.avatar_manager.avatarsById)
        game_state.world_map.reconstruct_interactive_state(num_avatars)

    def run_turn(self):
        try:
            game_state = world_state_provider.lock_and_get_world()

            for avatar in game_state.avatar_manager.avatarsById.values():
                avatar.handle_turn(game_state.get_state_for(avatar)).apply(game_state, avatar)

            self._update_environment(game_state)

        finally:
            world_state_provider.release_lock()

    def run_game(self):
        while True:
            self.run_turn()
            time.sleep(0.5)
