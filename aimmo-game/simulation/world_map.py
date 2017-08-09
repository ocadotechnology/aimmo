import math
import random
from logging import getLogger

from pickups import ALL_PICKUPS
from world_state import MapFeature

DEFAULT_LEVEL_SETTINGS = {
    'TARGET_NUM_CELLS_PER_AVATAR': 0,
    'TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR': 0,
    'SCORE_DESPAWN_CHANCE': 0,
    'TARGET_NUM_PICKUPS_PER_AVATAR': 0,
    'PICKUP_SPAWN_CHANCE': 0,
    'NO_FOG_OF_WAR_DISTANCE': 1000,
    'PARTIAL_FOG_OF_WAR_DISTANCE': 1000,
}

from simulation.action import MoveAction
from simulation.location import Location

LOGGER = getLogger(__name__)

class Cell(object):
    """
    Any position on the world grid.
    """

    def __init__(self, location, habitable=True, generates_score=False, partially_fogged=False):
        self.location = location
        self.habitable = habitable
        self.generates_score = generates_score
        self.avatar = None
        self.pickup = None
        self.partially_fogged = partially_fogged
        self.actions = []

        # Used to update the map features in the current view of the user (score points on pickups).
        self.remove_from_scene = None
        self.add_to_scene = None

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={} f{})'.format(
            self.location, self.habitable, self.generates_score, self.avatar, self.pickup, self.partially_fogged)

    def __eq__(self, other):
        return self.location == other.location

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.location)

    @property
    def moves(self):
        return [move for move in self.actions if isinstance(move, MoveAction)]

    @property
    def is_occupied(self):
        return self.avatar is not None

    def serialise(self):
        if self.partially_fogged:
            return {
                'generates_score': self.generates_score,
                'location': self.location.serialise(),
                'partially_fogged': self.partially_fogged
            }
        else:
            return {
                'avatar': self.avatar.serialise() if self.avatar else None,
                'generates_score': self.generates_score,
                'habitable': self.habitable,
                'location': self.location.serialise(),
                'pickup': self.pickup.serialise() if self.pickup else None,
                'partially_fogged': self.partially_fogged
            }

########################################################################################################

class BasicWorldMap(object):
    """
        A BasicWorldMap from which World Map inherits from.

        Its purpose is to keep only the basic getters.
    """
    def __init__(self, grid, settings):
        self.grid = grid
        self.settings = settings

    def is_on_map(self, location):
        try:
            self.grid[location]
        except KeyError:
            return False
        return True

    def get_cell(self, location):
        if self.is_on_map(location):
            return self.grid[location]
        raise ValueError('Location %s is not on the map' % location)
    def all_cells(self):
        return self.grid.itervalues()
    def score_cells(self):
        return (c for c in self.all_cells() if c.generates_score)
    def pickup_cells(self):
        return (c for c in self.all_cells() if c.pickup)

    def max_y(self):
        return max(self.grid.keys(), key=lambda c: c.y).y
    def min_y(self):
        return min(self.grid.keys(), key=lambda c: c.y).y
    def max_x(self):
        return max(self.grid.keys(), key=lambda c: c.x).x
    def min_x(self):
        return min(self.grid.keys(), key=lambda c: c.x).x

    @property
    def num_rows(self):
        return self.max_y() - self.min_y() + 1
    @property
    def num_cols(self):
        return self.max_x() - self.min_x() + 1
    @property
    def num_cells(self):
        return self.num_rows * self.num_cols

class WorldMap(BasicWorldMap):
    """
    The non-player world state.

    WorldMap has the following API:
        Cells -- from BasicWorldMap
        - get_cell
        - all_cells
        - score_cells
        - pickup_cells

        Map -- from BasicWorldMap
        - is_on_map
        - max_x
        - max_y
        - min_x
        - min_y
        - num_cols
        - num_rows
        - num_cells

        Dependecies
        - update -- used by TurnManager to update the world at each frame
        - clear_cell_actions -- used by TurnManager to tell WorldMap to clear actions
        - cells_to_create -- used by WorldState to retreive the cells to view
            - used to know when to instantiate objects in the scene.
        - TODO: cells_to_delete

        Misc Dependecies
        - get_random_spawn_location - get a free habitable cell or IndexError
        - can_move_to - assert if avatar can move to location
        - attackable_avatar - return the avatar attackable at the given location, or None.
    """

    def __init__(self, grid, settings):
        self.grid = grid
        self.settings = settings

    def cells_to_create(self):
        new_cells = []
        for cell in self.all_cells():
            if not cell.created:
                new_cells.append(cell)
        return new_cells

    def clear_cell_actions(self, location):
        try:
            cell = self.get_cell(location)
            cell.actions = []
        except ValueError:
            return

    def update(self, num_avatars):
        self._update_avatars()
        self._update_map(num_avatars)

    def get_random_spawn_location(self):
        return self._get_random_spawn_locations(1)[0].location

    def can_move_to(self, target_location):
        if not self.is_on_map(target_location):
            return False
        cell = self.get_cell(target_location)

        return (cell.habitable
                and (not cell.is_occupied or cell.avatar.is_moving)
                and len(cell.moves) <= 1)

    def attackable_avatar(self, target_location):
        try:
            cell = self.get_cell(target_location)
        except ValueError:
            return None

        if cell.avatar:
            return cell.avatar

        if len(cell.moves) == 1:
            return cell.moves[0].avatar

        return None

    def get_no_fog_distance(self):
        return self.settings['NO_FOG_OF_WAR_DISTANCE']

    def get_partial_fog_distance(self):
        return self.settings['PARTIAL_FOG_OF_WAR_DISTANCE']

    def __repr__(self):
        return repr(self.grid)

    def __iter__(self):
        return ((self.get_cell(Location(x, y))
                for y in xrange(self.min_y(), self.max_y() + 1))
                for x in xrange(self.min_x(), self.max_x() + 1))

#############################################Interals###################################################

    """
        Update function called periodically. The update is done as:
            * _update avatars:
                _apply_score: each avatar receives a score
                _apply_pickups: each avatar grabs a pickup
            * _update_map:
                _expand: the map is expanded so that it fits the size of the avatars if more avatars arrive
                _reset_score_locations: new score locations are generated
                _add_pickups: new pickups are generated
    """

    def _update_avatars(self):
        self._apply_score()
        self._apply_pickups()

    def _apply_pickups(self):
        for cell in self.pickup_cells():
            if cell.avatar is not None:
                cell.pickup.apply(cell.avatar)

    def _apply_score(self):
        for cell in self.score_cells():
            try:
                cell.avatar.score += 1
            except AttributeError:
                pass

    def _update_map(self, num_avatars):
        self._expand(num_avatars)
        self._reset_score_locations(num_avatars)
        self._add_pickups(num_avatars)

    def _expand(self, num_avatars):
        #LOGGER.info('Expanding map')
        start_size = self.num_cells
        target_num_cells = int(math.ceil(num_avatars * self.settings['TARGET_NUM_CELLS_PER_AVATAR']))
        num_cells_to_add = target_num_cells - self.num_cells
        if num_cells_to_add > 0:
            self._add_outer_layer()
            assert self.num_cells > start_size

    def _add_outer_layer(self):
        self._add_vertical_layer(self.min_x() - 1)
        self._add_vertical_layer(self.max_x() + 1)
        self._add_horizontal_layer(self.min_y() - 1)
        self._add_horizontal_layer(self.max_y() + 1)

    def _add_vertical_layer(self, x):
        for y in xrange(self.min_y(), self.max_y() + 1):
            self.grid[Location(x, y)] = Cell(Location(x, y))

    def _add_horizontal_layer(self, y):
        for x in xrange(self.min_x(), self.max_x() + 1):
            self.grid[Location(x, y)] = Cell(Location(x, y))

    def _reset_score_locations(self, num_avatars):
        for cell in self.score_cells():
            if random.random() < self.settings['SCORE_DESPAWN_CHANCE']:
                # Remove the score point from the scene if there was one.
                if cell.generates_score:
                    cell.remove_from_scene = MapFeature.SCORE_POINT
                cell.generates_score = False

        new_num_score_locations = len(list(self.score_cells()))
        target_num_score_locations = int(math.ceil(
            num_avatars * self.settings['TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR']
        ))
        num_score_locations_to_add = target_num_score_locations - new_num_score_locations
        locations = self._get_random_spawn_locations(num_score_locations_to_add)
        for cell in locations:
            # Add the score point to the scene if there wasn't one.
            if not cell.generates_score:
                cell.add_to_scene = MapFeature.SCORE_POINT
            cell.generates_score = True

    def _add_pickups(self, num_avatars):
        target_num_pickups = int(math.ceil(num_avatars * self.settings['TARGET_NUM_PICKUPS_PER_AVATAR']))
        LOGGER.debug('Aiming for %s new pickups', target_num_pickups)
        max_num_pickups_to_add = target_num_pickups - len(list(self.pickup_cells()))
        locations = self._get_random_spawn_locations(max_num_pickups_to_add)
        for cell in locations:
            if random.random() < self.settings['PICKUP_SPAWN_CHANCE']:
                LOGGER.info('Adding new pickup at %s', cell)
                cell.pickup = random.choice(ALL_PICKUPS)(cell)

    def _get_random_spawn_locations(self, max_locations):
        if max_locations <= 0:
            return []
        potential_locations = list(self.potential_spawn_locations())
        try:
            return random.sample(potential_locations, max_locations)
        except ValueError:
            LOGGER.debug('Not enough potential locations')
            return potential_locations

    # only exposed for testing
    def potential_spawn_locations(self):
        return (c for c in self.all_cells()
                if c.habitable
                and not c.generates_score
                and not c.avatar
                and not c.pickup)

##############################################################################################################


def WorldMapStaticSpawnDecorator(world_map, spawn_location):
    world_map.get_random_spawn_location = lambda: spawn_location
    return world_map
