import math
import random

from location import Location

# TODO: extract to settings
TARGET_NUM_CELLS_PER_AVATAR = 16

TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 0.5
SCORE_DESPAWN_CHANCE = 0.02

TARGET_NUM_PICKUPS_PER_AVATAR = 0.5
PICKUP_SPAWN_CHANCE = 0.02

NO_FOG_OF_WAR_DISTIANCE = 2
PARTIAL_FOG_OF_WAR_DISTIANCE = 3


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

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={} f{})'.format(self.location, self.habitable, self.generates_score, self.avatar, self.pickup, self.partially_fogged)

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def serialise(self):
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
        self.grid = grid

    def all_cells(self):
        return (cell for sublist in self.grid for cell in sublist)

    def score_cells(self):
        return (c for c in self.all_cells() if c.generates_score)

    def potential_spawn_locations(self):
        return (c for c in self.all_cells() if c.habitable and not c.generates_score and not c.avatar and not c.pickup)

    def pickup_cells(self):
        return (c for c in self.all_cells() if c.pickup)

    def is_on_map(self, location):
        return (0 <= location.y < self.num_rows) and (0 <= location.x < self.num_cols)

    def get_cell(self, location):
        if not self.is_on_map(location):
            raise ValueError('Location %s is not on the map' % location)
        cell = self.grid[location.x][location.y]
        assert cell.location == location, 'location lookup mismatch: arg={}, found={}'.format(location, cell.location)
        return cell

    @property
    def num_rows(self):
        return len(self.grid[0])

    @property
    def num_cols(self):
        return len(self.grid)

    @property
    def num_cells(self):
        return self.num_rows * self.num_cols

    def reconstruct_interactive_state(self, num_avatars):
        self.expand(num_avatars)
        self.reset_score_locations(num_avatars)
        self.add_pickups(num_avatars)

    def expand(self, num_avatars):
        target_num_cells = int(math.ceil(num_avatars * TARGET_NUM_CELLS_PER_AVATAR))
        num_cells_to_add = target_num_cells - self.num_cells
        if num_cells_to_add > 0:
            self.add_outer_layer()

    def add_outer_layer(self):
        self.add_layer_to_vertical_edge()
        self.add_layer_to_horizontal_edge()

    def add_layer_to_vertical_edge(self):
        self.grid.append([Cell(Location(self.num_cols, y)) for y in range(self.num_rows)])

    def add_layer_to_horizontal_edge(self):
        rows = self.num_rows  # Read rows once here, as we'll mutate it as part of the first iteration
        for x in range(self.num_cols):
            self.grid[x].append(Cell(Location(x, rows)))

    def reset_score_locations(self, num_avatars):
        for cell in self.score_cells():
            if random.random() < SCORE_DESPAWN_CHANCE:
                cell.generates_score = False

        new_num_score_locations = len(list(self.score_cells()))
        target_num_score_locations = int(math.ceil(num_avatars * TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR))
        num_score_locations_to_add = target_num_score_locations - new_num_score_locations
        if num_score_locations_to_add > 0:
            for cell in random.sample(list(self.potential_spawn_locations()), num_score_locations_to_add):
                cell.generates_score = True

    def add_pickups(self, num_avatars):
        target_num_pickups = int(math.ceil(num_avatars * TARGET_NUM_PICKUPS_PER_AVATAR))
        max_num_pickups_to_add = target_num_pickups - len(list(self.pickup_cells()))
        if max_num_pickups_to_add > 0:
            for cell in random.sample(list(self.potential_spawn_locations()), max_num_pickups_to_add):
                if random.random() < PICKUP_SPAWN_CHANCE:
                    cell.pickup = HealthPickup()

    def get_random_spawn_location(self):
        return random.choice(list(self.potential_spawn_locations())).location

    # TODO: cope with negative coords (here and possibly in other places)
    def can_move_to(self, target_location):
        if not self.is_on_map(target_location):
            return False

        cell = self.get_cell(target_location)
        return cell.habitable and not cell.avatar

    def get_no_fog_distance(self):
        return NO_FOG_OF_WAR_DISTIANCE

    def get_partial_fog_distance(self):
        return PARTIAL_FOG_OF_WAR_DISTIANCE

    def __repr__(self):
        return repr(self.grid)
