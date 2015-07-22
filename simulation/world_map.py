import random
import numpy as np
from simulation.direction import Direction


class SquareType:
    def __init__(self, name, key):
        self.name = name
        self.key = key

EMPTY = SquareType("empty", 0)
OBSTACLE = SquareType("obstacle", 1)
SCORE = SquareType("score", 2)


def generate_map(height, width, obstacle_ratio, scoring_square_ratio):
    matrix_of_level = np.empty((height, width), dtype=object)

    for y in xrange(height):
        for x in xrange(width):
            if random.random() < obstacle_ratio:
                matrix_of_level[y, x] = OBSTACLE
            elif random.random() < scoring_square_ratio:
                matrix_of_level[y, x] = SCORE
            else:
                matrix_of_level[y, x] = EMPTY

    return WorldMap(matrix_of_level)


# TODO: investigte switch from numpy to 2d lists to avoid making users know numpy and having to install it
class WorldMap(object):
    def __init__(self, grid):
        self.grid = grid

    # TODO: cope with negative coords (here and possibly in other places
    def can_move_to(self, target_location):
        num_rows, num_cols = self.grid.shape
        return (
            (0 <= target_location.row < num_rows)
            and (0 <= target_location.col < num_cols)
            and self.grid[target_location.row, target_location.col] != OBSTACLE
        )

    # TODO: switch to always deal in fixed coord space rather than floating origin
    def get_world_view_centred_at(self, view_location, distance_to_edge):
        """
                       world map = self.grid
        +-----------------------------------------------+
        |                                               |
        |                                               |
        |                                               |
        |                + view_map_corner              |
        |                |                              |
        |                v                              |
        |                     view map                  |   |
        |                +---------------+              |   | increasing
        |                |               |              |   |   rows
        |                |               |              |   |
        |                |       X       |              |   v
        |                |               |              |
        |                |               |              |
        |                +---------------+              |
        |                                               |
        |                                               |
        |                                               |
        |                                               |
        |                                               |
        +-----------------------------------------------+

                     -------------------->
                      increasing columns

        """
        num_grid_rows, num_grid_cols = self.grid.shape
        view_diameter = 2 * distance_to_edge + 1

        view_map_corner = view_location - Direction(distance_to_edge, distance_to_edge)

        # Non-cropped indices
        row_start = view_map_corner.row
        row_exclusive_end = row_start + view_diameter

        col_start = view_map_corner.col
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

        padded_view_map = np.pad(cropped_view_map,
                                 ((num_pad_rows_before, num_pad_rows_after), (num_pad_cols_before, num_pad_cols_after)),
                                 mode='constant', constant_values=-1
                                 )

        return padded_view_map
