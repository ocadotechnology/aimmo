import math
import random
from logging import getLogger

from simulation.pickups import ALL_PICKUPS
from simulation.action import MoveAction
from simulation.location import Location
from world_state import MapFeature

LOGGER = getLogger(__name__)

from simulation.world_state import MapFeature

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
from simulation.cell import *

LOGGER = getLogger(__name__)

class WorldMap(object):
    """
    The non-player world state.
    """

    def __init__(self, grid, settings):
        self.grid = grid
        self.settings = settings
    def all_cells(self):
        return self.grid.itervalues()

    # Used to know when to instantiate objects in the scene.
    def cells_to_create(self):
        new_cells = []
        for cell in self.all_cells():
            if not cell.created:
                new_cells.append(cell)
        return new_cells

    def score_cells(self):
        return (c for c in self.all_cells() if c.generates_score)

    def potential_spawn_locations(self):
        return (c for c in self.all_cells()
                if c.habitable
                and not c.generates_score
                and not c.avatar
                and not c.pickup)

    def pickup_cells(self):
        return (c for c in self.all_cells() if c.pickup)

    def is_on_map(self, location):
        try:
            self.grid[location]
        except KeyError:
            return False
        return True

    def get_cell(self, location):
        try:
            return self.grid[location]
        except KeyError:
            # For backwards-compatibility, this throws ValueError
            raise ValueError('Location %s is not on the map' % location)

    def get_cell_by_coords(self, x, y):
        return self.get_cell(Location(x, y))

    def clear_cell_actions(self, location):
        try:
            cell = self.get_cell(location)
            cell.actions = []
        except ValueError:
            return

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

    def update(self, num_avatars):
        # TODO: refactor into GameState (this class does too much)
        self._update_avatars()
        self._update_map(num_avatars)

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
                cell.cell_content = Floor({})

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
            cell.cell_content = ScoreLocation({})

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

    def get_random_spawn_location(self):
        """Return a single random spawn location.

        Throws:
            IndexError: if there are no possible locations.
        """
        return self._get_random_spawn_locations(1)[0].location

    def can_move_to(self, target_location):
        if not self.is_on_map(target_location):
            return False
        cell = self.get_cell(target_location)

        return (cell.habitable
                and (not cell.is_occupied or cell.avatar.is_moving)
                and len(cell.moves) <= 1)

    def attackable_avatar(self, target_location):
        """
        Return the avatar attackable at the given location, or None.
        """
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


def WorldMapStaticSpawnDecorator(world_map, spawn_location):
    world_map.get_random_spawn_location = lambda: spawn_location
    return world_map
