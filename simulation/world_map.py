import random
import math
from simulation.direction import Direction, ALL_DIRECTIONS
from simulation.location import Location


# TODO: extract to settings
TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 0.5
SCORE_DESPAWN_CHANCE = 0.02

TARGET_NUM_PICKUPS_PER_AVATAR = 0.5
PICKUP_SPAWN_CHANCE = 0.02


class HealthPickup(object):
    def __init__(self, health_restored=3):
        self.health_restored = health_restored

    def __repr__(self):
        return 'HealthPickup(health_restored={})'.format(self.health_restored)


class Cell(object):
    def __init__(self, location, habitable=True, generates_score=False):
        self.location = location
        self.habitable = habitable
        self.generates_score = generates_score
        self.avatar = None
        self.pickup = None

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={})'.format(self.location, self.habitable, self.generates_score, self.avatar, self.pickup)

    def __eq__(self, other):
        return self.location == other.location


def get_shortest_path_between(cell1, cell2, m):
    branches = [[cell1]]
    visited_cells = []

    while True:
        # TODO: avoid two lookups by using a priority queue and popping
        branch = min(branches, key=lambda b: len(b))
        branches.remove(branch)

        for cell in get_adjacent_habitable_cells(branch[-1], m):
            if cell in visited_cells:
                continue

            visited_cells.append(cell)

            new_branch = list(branch)
            new_branch.append(cell)

            if cell == cell2:
                return new_branch

            branches.append(new_branch)

        if not branches:
            return None


def get_adjacent_habitable_cells(cell, m):
    return [c for c in (m.get_cell(cell.location + d) for d in ALL_DIRECTIONS) if c and c.habitable]


def bisects_map(cell, m):
    adjacent_cells = get_adjacent_habitable_cells(cell, m)
    if len(adjacent_cells) < 2:
        return False

    last_cell = adjacent_cells[-1]
    for c in adjacent_cells[:-1]:
        if not get_shortest_path_between(c, last_cell, m):
            return True

    return False


def generate_map(height, width, obstacle_ratio):
    grid = [[Cell(Location(x, y)) for y in xrange(height)] for x in xrange(width)]
    m = WorldMap(grid)

    for x in xrange(width):
        for y in xrange(height):
            if random.random() < obstacle_ratio:
                cell = grid[x][y]
                cell.habitable = False
                if bisects_map(cell, m):
                    cell.habitable = True

    return m


class WorldMap(object):
    def __init__(self, grid):
        self.grid = grid

    def generate_all_cells(self):
        return (cell for sublist in self.grid for cell in sublist)

    @property
    def all_cells(self):
        return list(self.generate_all_cells())

    def generate_score_cells(self):
        return (c for c in self.generate_all_cells() if c.generates_score)

    def generate_potential_spawn_locations(self):
        return (c for c in self.generate_all_cells() if c.habitable and not c.generates_score and not c.avatar and not c.pickup)

    def generate_pickup_cells(self):
        return (c for c in self.generate_all_cells() if c.pickup)

    def is_on_map(self, location):
        num_cols = len(self.grid)
        num_rows = len(self.grid[0])
        return (0 <= location.y < num_rows) and (0 <= location.x < num_cols)

    def get_cell(self, location):
        if not self.is_on_map(location):
            return None
        cell = self.grid[location.x][location.y]
        assert cell.location == location, 'location lookup mismatch: arg={}, found={}'.format(location, cell.location)
        return cell

    def update(self, num_avatars):
        self.update_score_locations(num_avatars)
        self.update_pickups(num_avatars)

    def update_score_locations(self, num_avatars):
        for cell in self.generate_score_cells():
            if random.random() < SCORE_DESPAWN_CHANCE:
                cell.generates_score = False

        new_num_score_locations = len(list(self.generate_score_cells()))
        target_num_score_locations = int(math.ceil(num_avatars * TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR))
        num_score_locations_to_add = target_num_score_locations - new_num_score_locations
        if num_score_locations_to_add > 0:
            for cell in random.sample(list(self.generate_potential_spawn_locations()), num_score_locations_to_add):
                cell.generates_score = True

    def update_pickups(self, num_avatars):
        target_num_pickups = int(math.ceil(num_avatars * TARGET_NUM_PICKUPS_PER_AVATAR))
        max_num_pickups_to_add = target_num_pickups - len(list(self.generate_pickup_cells()))
        if max_num_pickups_to_add > 0:
            for cell in random.sample(list(self.generate_potential_spawn_locations()), max_num_pickups_to_add):
                if random.random() < PICKUP_SPAWN_CHANCE:
                    cell.pickup = HealthPickup()

    def get_random_spawn_location(self):
        return random.choice(list(self.generate_potential_spawn_locations())).location

    # TODO: cope with negative coords (here and possibly in other places)
    def can_move_to(self, target_location):
        if not self.is_on_map(target_location):
            return False

        cell = self.get_cell(target_location)
        return cell.habitable and not cell.avatar

    # TODO: switch to always deal in fixed coord space rather than floating origin
    # FIXME: make this work with list of lists instead of numpy
    # FIXME: make this work with x and y instead of row and col
    def get_world_view_centred_at(self, view_location, distance_to_edge):
        num_grid_rows, num_grid_cols = self.grid.shape
        view_diameter = 2 * distance_to_edge + 1

        view_map_corner = view_location - Direction(distance_to_edge, distance_to_edge)

        # Non-cropped indices
        row_start = view_map_corner.y
        row_exclusive_end = row_start + view_diameter

        col_start = view_map_corner.x
        col_exclusive_end = col_start + view_diameter

        # Cropped indices
        cropped_row_start = max(0, row_start)
        cropped_row_exclusive_end = min(num_grid_rows, row_start + view_diameter)

        cropped_col_start = max(0, col_start)
        cropped_col_exclusive_end = min(num_grid_cols, col_start + view_diameter)

        assert 0 <= cropped_row_start < cropped_row_exclusive_end <= num_grid_rows
        assert 0 <= cropped_col_start < cropped_col_exclusive_end <= num_grid_cols

        # Extract cropped region
        cropped_view_map = self.grid[cropped_row_start:cropped_row_exclusive_end, cropped_col_start:cropped_col_exclusive_end]

        # Pad map
        num_pad_rows_before = cropped_row_start - row_start
        num_pad_rows_after = row_exclusive_end - cropped_row_exclusive_end

        num_pad_cols_before = cropped_col_start - col_start
        num_pad_cols_after = col_exclusive_end - cropped_col_exclusive_end

        # padded_view_map = np.pad(cropped_view_map,
        #                          ((num_pad_rows_before, num_pad_rows_after), (num_pad_cols_before, num_pad_cols_after)),
        #                          mode='constant', constant_values=-1
        #                          )
        #
        # return padded_view_map

    def __repr__(self):
        return repr(self.grid)
