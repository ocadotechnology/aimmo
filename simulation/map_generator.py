import heapq
import random
from simulation.direction import ALL_DIRECTIONS
from simulation.location import Location
from simulation.world_map import Cell, WorldMap


def generate_map(height, width, obstacle_ratio):
    grid = [[Cell(Location(x, y)) for y in xrange(height)] for x in xrange(width)]
    world_map = WorldMap(grid)

    # We designate one (non-corner) edge cell as empty, with two effects:
    #   - We ensure that the map can be expanded
    #   - If we ensure that this cell is always reachable, then the map cannot get bisected
    edge_x, edge_y = get_random_edge_index(height, width)
    always_empty_edge_cell = grid[edge_x][edge_y]

    for x, y in shuffled(_get_edge_coordinates(height, width)):
        if (x, y) != (edge_x, edge_y) and random.random() < obstacle_ratio:
            cell = grid[x][y]
            cell.habitable = False
            if not _all_habitable_neighbours_of_cell1_can_reach_cell2(cell, always_empty_edge_cell, world_map):
                cell.habitable = True

    return world_map


def _get_edge_coordinates(height, width):
    for x in xrange(width):
        for y in xrange(height):
            yield x, y


def shuffled(iterable):
    values = list(iterable)
    random.shuffle(values)
    return iter(values)


def _all_habitable_neighbours_of_cell1_can_reach_cell2(cell1, cell2, world_map):
    neighbours = get_adjacent_habitable_cells(cell1, world_map)
    shortest_paths = (get_shortest_path_between(cell2, neighbour_cell, world_map) for neighbour_cell in neighbours)
    reachable = (path is not None for path in shortest_paths)
    return all(reachable)


def get_shortest_path_between(cell1, cell2, world_map):
    branches = PriorityQueue(key=lambda b: len(b), init_items=[[cell1]])
    visited_cells = set()

    while branches:
        branch = branches.pop()

        for cell in get_adjacent_habitable_cells(branch[-1], world_map):
            if cell in visited_cells:
                continue

            visited_cells.add(cell)

            new_branch = branch + [cell]

            if cell == cell2:
                return new_branch

            branches.push(new_branch)

    return None


def get_random_edge_index(height, width, rng=random):
    assert height >= 2 and width >= 2

    num_row_cells = width - 2
    num_col_cells = height - 2
    num_edge_cells = 2*num_row_cells + 2*num_col_cells
    random_cell = rng.randint(0, num_edge_cells-1)

    if 0 <= random_cell < num_row_cells:
        # random non-corner cell on the first row
        return random_cell+1, 0
    elif num_row_cells <= random_cell < 2*num_row_cells:
        # random non-corner cell on the last row
        random_cell -= num_row_cells
        return random_cell + 1, height - 1

    random_cell -= 2*num_row_cells

    if 0 <= random_cell < num_col_cells:
        # random non-corner cell on the first column
        return 0, random_cell + 1
    elif num_col_cells <= random_cell < 2*num_col_cells:
        # random non-corner cell on the last column
        random_cell -= num_col_cells
        return width - 1, random_cell + 1

    raise ValueError('Should not be reachable')


def get_adjacent_habitable_cells(cell, world_map):
    return [c for c in (world_map.get_cell(cell.location + d) for d in ALL_DIRECTIONS) if c and c.habitable]


class PriorityQueue(object):
    def __init__(self, key, init_items=[]):
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

