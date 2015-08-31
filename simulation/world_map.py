import random
import math
from simulation.direction import Direction
from simulation.location import Location


TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 0.5  # TODO: extract to settings
SCORE_DESPAWN_CHANCE = 0.02  # TODO: extract to settings


class Cell(object):
    def __init__(self, location, can_move_to=True, generates_score=False):
        self.location = location
        self.can_move_to = can_move_to
        self.generates_score = generates_score


def generate_map(height, width, obstacle_ratio):
    grid = [[None for x in xrange(width)] for y in xrange(height)]

    # TODO: ensure all cells that an avatar can_move_to are connected (no areas of the map are cut off from others)
    for x in xrange(width):
        for y in xrange(height):
            if random.random() < obstacle_ratio:
                grid[x][y] = Cell(Location(x, y), can_move_to=False)
            else:
                grid[x][y] = Cell(Location(x, y))

    return WorldMap(grid)


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

    def generate_occupiable_non_score_cells(self):
        return (c for c in self.generate_all_cells() if c.can_move_to and not c.generates_score)

    def is_on_map(self, location):
        num_cols = len(self.grid)
        num_rows = len(self.grid[0])
        return (0 <= location.y < num_rows) and (0 <= location.x < num_cols)

    def get_cell(self, location):
        cell = self.grid[location.x][location.y]
        assert cell.location == location, 'location lookup mismatch: arg={}, found={}'.format(location, cell.location)
        return cell

    def update_score_locations(self, num_avatars):
        for cell in self.generate_score_cells():
            if random.random() < SCORE_DESPAWN_CHANCE:
                cell.generates_score = False

        new_num_score_locations = len(list(self.generate_score_cells()))
        target_num_score_locations = int(math.ceil(num_avatars * TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR))
        num_score_locations_to_add = target_num_score_locations - new_num_score_locations
        if num_score_locations_to_add > 0:
            for cell in random.sample(list(self.generate_occupiable_non_score_cells()), num_score_locations_to_add):
                cell.generates_score = True

    def get_spawn_location(self):
        return random.choice(list(self.generate_occupiable_non_score_cells())).location

    # TODO: cope with negative coords (here and possibly in other places)
    def can_move_to(self, target_location):
        return self.is_on_map(target_location) and self.get_cell(target_location).can_move_to

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
