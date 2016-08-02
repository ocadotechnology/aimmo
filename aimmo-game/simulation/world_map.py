import math
import random

from logging import getLogger

from simulation.location import Location
from simulation.action import MoveAction

LOGGER = getLogger(__name__)

# TODO: extract to settings
TARGET_NUM_CELLS_PER_AVATAR = 16

TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 0.5
SCORE_DESPAWN_CHANCE = 0.02

TARGET_NUM_PICKUPS_PER_AVATAR = 0.5
PICKUP_SPAWN_CHANCE = 0.02

NO_FOG_OF_WAR_DISTANCE = 2
PARTIAL_FOG_OF_WAR_DISTANCE = 3


class HealthPickup(object):
    def __init__(self, health_restored=3):
        self.health_restored = health_restored

    def __repr__(self):
        return 'HealthPickup(health_restored={})'.format(self.health_restored)

    def serialise(self):
        return {
            'health_restored': self.health_restored,
        }


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

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={} f{})'.format(self.location, self.habitable, self.generates_score, self.avatar, self.pickup, self.partially_fogged)

    def __eq__(self, other):
        return self.location == other.location

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


class WorldMap(object):
    """
    The non-player world state.
    """

    def __init__(self, grid):
        try:
            grid[Location(0, 0)]
        except TypeError:
            self._convert_grid_from_list(grid)
        except KeyError:
            # Allow an empty grid
            self._grid = grid
        else:
            self._grid = grid

    def _convert_grid_from_list(self, grid):
        self._grid = {cell.location: cell for row in grid for cell in row}

    def all_cells(self):
        return self._grid.itervalues()

    def score_cells(self):
        return (c for c in self.all_cells() if c.generates_score)

    def potential_spawn_locations(self):
        return (c for c in self.all_cells()
                if c.habitable and not c.generates_score and not c.avatar and
                not c.pickup)

    def pickup_cells(self):
        return (c for c in self.all_cells() if c.pickup)

    def is_on_map(self, location):
        try:
            self._grid[location]
        except KeyError:
            return False
        return True

    def get_cell(self, location):
        try:
            return self._grid[location]
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

    def _max_y(self):
        max_y = 0
        while True:
            try:
                self._grid[Location(0, max_y)]
            except KeyError:
                max_y -= 1
                break
            else:
                max_y += 1
        return max_y

    def min_y(self):
        min_y = 0
        while True:
            try:
                self._grid[Location(0, min_y)]
            except KeyError:
                min_y += 1
                break
            else:
                min_y -= 1
        return min_y

    @property
    def num_rows(self):
        return self._max_y() - self.min_y() + 1

    def _max_x(self):
        max_x = 0
        while True:
            try:
                self._grid[Location(max_x, 0)]
            except KeyError:
                max_x -= 1
                break
            else:
                max_x += 1
        return max_x

    def min_x(self):
        min_x = 0
        while True:
            try:
                self._grid[Location(min_x, 0)]
            except KeyError:
                min_x += 1
                break
            else:
                min_x -= 1
        return min_x

    @property
    def num_cols(self):
        return self._max_x() - self.min_x() + 1

    @property
    def num_cells(self):
        return self.num_rows * self.num_cols

    def apply_score(self):
        for cell in self.score_cells():
            try:
                cell.avatar.score += 1
            except AttributeError:
                pass

    def reconstruct_interactive_state(self, num_avatars):
        self._expand(num_avatars)
        self._reset_score_locations(num_avatars)
        self._add_pickups(num_avatars)

    def _expand(self, num_avatars):
        LOGGER.info('Expanding map')
        start_size = self.num_cells
        target_num_cells = int(math.ceil(num_avatars * TARGET_NUM_CELLS_PER_AVATAR))
        num_cells_to_add = target_num_cells - self.num_cells
        if num_cells_to_add > 0:
            self._add_outer_layer()
            assert self.num_cells > start_size

    def _add_outer_layer(self):
        self._add_vertical_layer(self.min_x()-1)
        self._add_vertical_layer(self._max_x()+1)
        self._add_horizontal_layer(self.min_y()-1)
        self._add_horizontal_layer(self._max_y()+1)

    def _add_vertical_layer(self, x):
        for y in xrange(self.min_y(), self._max_y()+1):
            self._grid[Location(x, y)] = Cell(Location(x, y))

    def _add_horizontal_layer(self, y):
        for x in xrange(self.min_x(), self._max_x()+1):
            self._grid[Location(x, y)] = Cell(Location(x, y))

    def _reset_score_locations(self, num_avatars):
        for cell in self.score_cells():
            if random.random() < SCORE_DESPAWN_CHANCE:
                cell.generates_score = False

        new_num_score_locations = len(list(self.score_cells()))
        target_num_score_locations = int(math.ceil(
            num_avatars * TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR
        ))
        num_score_locations_to_add = target_num_score_locations - new_num_score_locations
        locations = self._get_random_spawn_locations(num_score_locations_to_add)
        for cell in locations:
            cell.generates_score = True

    def _add_pickups(self, num_avatars):
        target_num_pickups = int(math.ceil(num_avatars * TARGET_NUM_PICKUPS_PER_AVATAR))
        LOGGER.debug('Aiming for %s new pickups', target_num_pickups)
        max_num_pickups_to_add = target_num_pickups - len(list(self.pickup_cells()))
        locations = self._get_random_spawn_locations(max_num_pickups_to_add)
        for cell in locations:
            if random.random() < PICKUP_SPAWN_CHANCE:
                LOGGER.info('Adding new pickup at %s', cell)
                cell.pickup = HealthPickup()

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
        '''
        Return the avatar attackable at the given location, or None.
        '''
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
        return NO_FOG_OF_WAR_DISTANCE

    def get_partial_fog_distance(self):
        return PARTIAL_FOG_OF_WAR_DISTANCE

    def __repr__(self):
        return repr(self._grid)

    def __iter__(self):
        return ((self.get_cell(Location(x, y))
                for y in xrange(self.min_y(), self._max_y()+1))
                for x in xrange(self.min_x(), self._max_x()+1))
