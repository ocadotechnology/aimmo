import abc
import heapq
import logging
import random
from itertools import tee

from six.moves import zip, range

from simulation.direction import ALL_DIRECTIONS
from simulation.game_state import GameState
from simulation.location import Location
from simulation.world_map import WorldMap
from simulation.world_map import WorldMapStaticSpawnDecorator
from simulation.world_map import DEFAULT_LEVEL_SETTINGS

from simulation.custom_map import BaseGenerator
from simulation.custom_map import BaseLevelGenerator
from simulation.custom_map import Level1
from simulation.custom_map import EmptyMapGenerator

LOGGER = logging.getLogger(__name__)

class Main(BaseGenerator):

    """
        Main Level generator used by the map creation service from the Django server.
        Custom level generators(see package levels) can be found in @custom_map.
        To read more about map generators, read documentation in custom_map.

        Obstacles are filled according to the obstacle ratio.

        Once an obstacle is added we ensure that each habitable cell can reach each other,
        thus the map will be connex and each generated avatar can reach others.
    """
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        self.settings.update(DEFAULT_LEVEL_SETTINGS)

        # Fix for  'NO_FOG_OF_WAR_DISTANCE' bug
        if not 'NO_FOG_OF_WAR_DISTANCE' in self.settings.keys():
            self.settings['NO_FOG_OF_WAR_DISTANCE'] = DEFAULT_LEVEL_SETTINGS['NO_FOG_OF_WAR_DISTANCE']

    def get_map(self):
        height = self.settings['START_HEIGHT']
        width = self.settings['START_WIDTH']
        world_map = EmptyMapGenerator(height, width, self.settings).get_map()

        # We designate one non-corner edge cell as empty, to ensure that the map can be expanded
        always_empty_edge_x, always_empty_edge_y = get_random_edge_index(world_map)
        always_empty_location = Location(always_empty_edge_x, always_empty_edge_y)

        for cell in shuffled(world_map.all_cells()):
            if cell.location != always_empty_location and random.random() < self.settings['OBSTACLE_RATIO']:
                cell.habitable = False
                # So long as all habitable neighbours can still reach each other,
                # then the map cannot get bisected
                if not _all_habitable_neighbours_can_reach_each_other(cell, world_map):
                    cell.habitable = True

        return world_map


def _get_edge_coordinates(height, width):
    for x in range(width):
        for y in range(height):
            yield x, y


def shuffled(iterable):
    values = list(iterable)
    random.shuffle(values)
    return iter(values)


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def _all_habitable_neighbours_can_reach_each_other(cell, world_map):
    """
        Helper function used by Main map generator. It ensures that each habitable cell can
        reach each other.
    """
    neighbours = get_adjacent_habitable_cells(cell, world_map)

    assert len(neighbours) >= 1
    neighbour_pairs = ((n1, n2) for n1, n2 in pairwise(neighbours))
    shortest_path_exists = (get_shortest_path_between(n1, n2, world_map) is not None
                            for n1, n2 in neighbour_pairs)
    return all(shortest_path_exists)


def get_shortest_path_between(source_cell, destination_cell, world_map):
    """
        Helper function. Uses A* to find the a shortest path between two cells.
        The chosen admisible heuristic function is the manhattan function.
    """
    def manhattan_distance_to_destination_cell(this_branch):
        branch_tip_location = this_branch[-1].location
        x_distance = abs(branch_tip_location.x - destination_cell.location.x)
        y_distance = abs(branch_tip_location.y - destination_cell.location.y)
        return x_distance + y_distance + len(this_branch)

    branches = PriorityQueue(key=manhattan_distance_to_destination_cell, init_items=[[source_cell]])
    visited_cells = set()

    while branches:
        branch = branches.pop()

        for cell in get_adjacent_habitable_cells(branch[-1], world_map):
            if cell in visited_cells:
                continue

            visited_cells.add(cell)

            new_branch = branch + [cell]

            if cell == destination_cell:
                return new_branch

            branches.push(new_branch)

    return None


def get_random_edge_index(world_map, rng=random):
    """
        Utility function used to get a tuple (x, y) on the edge of the map.
        Note the function returns a tuple rather than a Location.

        This function is also used by the tests.
    """
    num_row_cells = world_map.num_rows - 2
    num_col_cells = world_map.num_cols - 2
    num_edge_cells = 2*num_row_cells + 2*num_col_cells
    random_cell = rng.randint(0, num_edge_cells-1)

    if 0 <= random_cell < num_col_cells:
        # random non-corner cell on the first row
        return random_cell + 1 + world_map.min_x(), world_map.min_y()
    random_cell -= num_col_cells

    if 0 <= random_cell < num_col_cells:
        # random non-corner cell on the last row
        return random_cell + 1 + world_map.min_x(), world_map.max_y()
    random_cell -= num_col_cells

    if 0 <= random_cell < num_row_cells:
        # random non-corner cell on the first column
        return world_map.min_x(), world_map.min_y() + random_cell + 1
    random_cell -= num_row_cells

    assert 0 <= random_cell < num_row_cells
    # random non-corner cell on the last column
    return world_map.max_x(), world_map.min_y() + random_cell + 1


def get_adjacent_habitable_cells(cell, world_map):
    adjacent_locations = [cell.location + d for d in ALL_DIRECTIONS]
    adjacent_locations = [location for location in adjacent_locations
                          if world_map.is_on_map(location)]

    adjacent_cells = [world_map.get_cell(location) for location in adjacent_locations]
    return [c for c in adjacent_cells if c.habitable]


class PriorityQueue(object):
    """
        Class used in the A* implementation.
    """
    def __init__(self, key, init_items=tuple()):
        self.key = key
        self.heap = [self._build_tuple(i) for i in init_items]
        heapq.heapify(self.heap)

    def _build_tuple(self, item):
        return self.key(item), item

    def push(self, item):
        to_push = self._build_tuple(item)
        heapq.heappush(self.heap, to_push)

    def pop(self):
        _, item = heapq.heappop(self.heap)
        return item

    def __len__(self):
        return len(self.heap)
