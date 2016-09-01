from threading import RLock

from simulation.avatar import fog_of_war
from simulation.location import Location


def alters_state(method):
    '''
    Decorator for methods that will modify the game state. Ensures that the
    edit lock is acquired.
    '''
    def wrapper(*args, **kwargs):
        self = args[0]
        with self._edit_lock:
            return method(*args, **kwargs)
    return wrapper


class GameState(object):
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """
    def __init__(self, world_map, avatar_manager):
        self._avatar_manager = avatar_manager
        self._world_map = world_map
        self._edit_lock = RLock()

    def __enter__(self):
        self._edit_lock.acquire()
        return self

    def __exit__(self, type, value, traceback):
        self._edit_lock.release()

    def view(self, avatar_id, fog_of_war=fog_of_war):
        '''
        Return the subset of the game state visible to an avatar.
        '''
        avatar = self._avatar_manager.get_avatar(avatar_id)
        fogged_map = fog_of_war.apply_fog_of_war(self._world_map, avatar)
        return {
            'avatar_state': avatar.serialise(),
            'world_map': {
                'cells': [cell.serialise() for cell in fogged_map.all_cells]
            }
        }

    @staticmethod
    def _cell_type(cell):
        return 1 if not cell.is_habitable else 2 if cell.generates_score else 0

    def snapshot(self):
        world = [[self._cell_type(self._world_map.get_cell(Location(x, y)))
                  for y in range(self._world_map.num_rows)]
                 for x in range(self._world_map.num_cols)]

        avatars = {avatar.user_id: avatar.snapshot()
                   for avatar in self._avatar_manager.active_avatars}

        return {
            'players': avatars,
            'layout': world,
            'width': self._world_map.num_cols,
            'height': self._world_map.num_rows,
            'score_locations': [(cell.location.x, cell.location.y)
                                for cell in self._world_map.score_cells],
            'pickup_locations': [(cell.location.x, cell.location.y)
                                 for cell in self._world_map.pickup_cells],
            'map_changed': True,
        }

    # Avatar methods ----------------------------------------------------------

    @property
    def active_avatars(self):
        return (avatar.user_id for avatar in self._avatar_manager.active_avatars)

    def avatar_location(self, avatar_id):
        return self._avatar_manager.get_avatar(avatar_id).location

    def avatar_at(self, location):
        try:
            return self._world_map.get_cell(location).avatar.user_id
        except AttributeError:
            return None

    def decide_action(self, avatar_id):
        avatar = self._avatar_manager.get_avatar(avatar_id)
        return avatar.decide_action(self.view(avatar_id))

    @alters_state
    def add_avatar(self, avatar_id, worker_url, location=None):
        avatar = self._avatar_manager.add_avatar(avatar_id, worker_url)
        self._avatar_manager.spawn(self._world_map, avatar, location)

    @alters_state
    def remove_avatar(self, avatar_id):
        try:
            avatar = self._avatar_manager.get_avatar(avatar_id)
        except KeyError:
            return
        self._world_map.get_cell(avatar.location).avatar = None
        self._avatar_manager.remove_avatar(avatar_id)

    @alters_state
    def move_avatar(self, avatar_id, direction):
        avatar = self._avatar_manager.get_avatar(avatar_id)

        self._world_map.get_cell(avatar.location).avatar = None
        avatar.location += direction
        self._world_map.get_cell(avatar.location).avatar = avatar

    @alters_state
    def hurt_avatar(self, avatar_id, damage):
        avatar = self._avatar_manager.get_avatar(avatar_id)
        avatar.health = max(0, avatar.health - damage)

    @alters_state
    def heal_avatar(self, avatar_id, health):
        self._avatar_manager.get_avatar(avatar_id).health += health

    @alters_state
    def add_event(self, avatar_id, event):
        self._avatar_manager.get_avatar(avatar_id).add_event(event)

    # World methods -----------------------------------------------------------

    @property
    def world_size(self):
        return (self._world_map.num_cols, self._world_map.num_rows)

    def cell_on_map(self, location):
        return self._world_map.cell_on_map(location)

    def cell_habitable(self, location):
        try:
            return self._world_map.get_cell(location).is_habitable
        except ValueError:
            return False

    def cell_occupied(self, location):
        try:
            return self._world_map.get_cell(location).is_occupied
        except ValueError:
            return False

    # Other methods -----------------------------------------------------------

    @alters_state
    def _apply_pickups(self):
        for cell in self._world_map.pickup_cells:
            pass  # TODO: apply pickup to avatar in cell.

    @alters_state
    def _apply_score(self):
        for cell in self._world_map.score_cells:
            try:
                cell.avatar.score += 1
            except AttributeError:
                pass

    @alters_state
    def end_of_turn(self):
        self._world_map.expand(self._avatar_manager.num_avatars)
        self._world_map.reset_score_locations(self._avatar_manager.num_avatars)
        self._world_map.add_pickups(self._avatar_manager.num_avatars)

        self._avatar_manager.process_deaths(self._world_map)

        self._apply_pickups()
        self._apply_score()
