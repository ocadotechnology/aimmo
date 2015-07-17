from threading import Lock

class WorldStateProvider:

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

    def _update_environment(self):
        pass

    def run_turn(self):
        world_state = world_state_provider.lock_and_get_world()

        self._update_environment()

        actions = [(p, p.handle_turn(self.world_state.get_state_for(p))) for p in world_state.avatar_manager.avatarsById.values()]
        for avatar, action in actions:
            action.apply(self.world_state, avatar)

        world_state_provider.release_lock()

    def run_game(self):
        while True:
            self.run_turn()
