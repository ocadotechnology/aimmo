import heapq
import random
from simulation.direction import ALL_DIRECTIONS
from simulation.location import Location
from simulation.world_map import Cell, WorldMap


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


def get_shortest_path_between(cell1, cell2, m):
    branches = PriorityQueue(key=lambda b: len(b), init_items=[[cell1]])
    visited_cells = set()

    while branches:
        branch = branches.pop()

        for cell in get_adjacent_habitable_cells(branch[-1], m):
            if cell in visited_cells:
                continue

            visited_cells.add(cell)

            new_branch = branch + [cell]

            if cell == cell2:
                return new_branch

            branches.push(new_branch)

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

