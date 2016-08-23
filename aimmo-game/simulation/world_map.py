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
        self._location = location
        self._habitable = habitable
        self.generates_score = generates_score
        self.avatar = None
        self.pickup = None
        self.partially_fogged = partially_fogged
        self._actions = []

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={} f{})'.format(self.location, self.habitable, self.generates_score, self.avatar, self.pickup, self.partially_fogged)

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    @property
    def location(self):
        return self._location

    @property
    def habitable(self):
        return self._habitable

    @property
    def actions(self):
        return [action for action in self._actions]

    @property
    def moves(self):
        return [move for move in self.actions if isinstance(move, MoveAction)]

    @property
    def is_occupied(self):
        return self.avatar is not None

    def register_action(self, action):
        self._actions.append(action)

    def clear_actions(self):
        self._actions = []

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
        self._grid = grid

    def all_cells(self):
        return (cell for row in self._grid for cell in row)

    def score_cells(self):
        return (c for c in self.all_cells() if c.generates_score)

    def potential_spawn_locations(self):
        return (c for c in self.all_cells()
                if c.habitable and not c.generates_score and not c.avatar and
                not c.pickup)

    def pickup_cells(self):
        return (c for c in self.all_cells() if c.pickup)

    def is_on_map(self, location):
        return (0 <= location.y < self.num_rows) and (0 <= location.x < self.num_cols)

    def get_cell(self, location):
        if not self.is_on_map(location):
            raise ValueError('Location %s is not on the map' % location)
        cell = self._grid[location.x][location.y]
        assert cell.location == location, 'location lookup mismatch: arg={}, found={}'.format(location, cell.location)
        return cell

    def clear_cell_actions(self, location):
        try:
            cell = self.get_cell(location)
            cell.clear_actions()
        except ValueError:
            return

    @property
    def num_rows(self):
        return len(self._grid[0])

    @property
    def num_cols(self):
        return len(self._grid)

    @property
    def num_cells(self):
        return self.num_rows * self.num_cols

    def apply_score(self):
        for cell in self.score_cells():
            try:
                cell.avatar.score += 1
            except AttributeError:
                pass

    def expand(self, num_avatars):
        target_num_cells = int(math.ceil(num_avatars * TARGET_NUM_CELLS_PER_AVATAR))
        num_cells_to_add = target_num_cells - self.num_cells
        if num_cells_to_add > 0:
            self._add_outer_layer()

    def _add_outer_layer(self):
        self._add_layer_to_vertical_edge()
        self._add_layer_to_horizontal_edge()

    def _add_layer_to_vertical_edge(self):
        self._grid.append([Cell(Location(self.num_cols, y)) for y in range(self.num_rows)])

    def _add_layer_to_horizontal_edge(self):
        # Read rows once here, as we'll mutate it as part of the first iteration
        rows = self.num_rows
        for x in range(self.num_cols):
            self._grid[x].append(Cell(Location(x, rows)))

    def reset_score_locations(self, num_avatars):
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

    def add_pickups(self, num_avatars):
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

    # TODO: cope with negative coords (here and possibly in other places)
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
