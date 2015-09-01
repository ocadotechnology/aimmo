import time
from threading import Lock
from simulation import world_map


class WorldStateProvider:
    """TODO: think about changing to snapshot rather than lock?"""
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
    def __init__(self, world_state):
        world_state_provider.set_world(world_state)

    def _update_environment(self, world_state):
        num_avatars = len(world_state.avatar_manager.avatarsById)
        world_state.world_map.update_score_locations(num_avatars)

    def run_turn(self):
        try:
            world_state = world_state_provider.lock_and_get_world()

            for avatar in world_state.avatar_manager.avatarsById.values():
                avatar.handle_turn(world_state.get_state_for(avatar)).apply(world_state, avatar)

            self._update_environment(world_state)

        finally:
            world_state_provider.release_lock()

    def run_game(self):
        while True:
            self.run_turn()
            time.sleep(0.5)
