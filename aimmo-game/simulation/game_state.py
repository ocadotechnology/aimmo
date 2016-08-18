from threading import Lock

from simulation.avatar import fog_of_war


def alters_state(method):
    '''
    Decorator for methods that will modify the game state. Checks that the
    edit lock is acquired.
    '''
    def wrapper(*args, **kwargs):
        self = args[0]
        assert self._edit_lock.locked(), 'Method requires edit lock!'
        return method(*args, **kwargs)
    return wrapper


class GameState(object):
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """
    def __init__(self, world_map, avatar_manager):
        self.world_map = world_map
        self.avatar_manager = avatar_manager

        self._edit_lock = Lock()

    def __enter__(self):
        self._edit_lock.acquire()
        return self

    def __exit__(self, type, value, traceback):
        self._edit_lock.release()

    def get_state_for(self, avatar_wrapper, fog_of_war=fog_of_war):
        processed_world_map = fog_of_war.apply_fog_of_war(self.world_map, avatar_wrapper)
        return {
            'avatar_state': avatar_wrapper.serialise(),
            'world_map': {
                'cells': [cell.serialise() for cell in processed_world_map.all_cells()]
            }
        }

    @alters_state
    def add_avatar(self, user_id, worker_url, location=None):
        location = self.world_map.get_random_spawn_location() if location is None else location
        avatar = self.avatar_manager.add_avatar(user_id, worker_url, location)
        self.world_map.get_cell(location).avatar = avatar

    @alters_state
    def remove_avatar(self, user_id):
        try:
            avatar = self.avatar_manager.get_avatar(user_id)
        except KeyError:
            return
        self.world_map.get_cell(avatar.location).avatar = None
        self.avatar_manager.remove_avatar(user_id)

    def update_environment(self):
        num_avatars = len(self.avatar_manager.active_avatars)
        self.world_map.reconstruct_interactive_state(num_avatars)
