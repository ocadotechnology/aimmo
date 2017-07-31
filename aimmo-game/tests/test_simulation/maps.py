from __future__ import absolute_import

from collections import defaultdict

from simulation.location import Location
from simulation.world_map import WorldMap
from simulation.cell import *

class MockPickup(object):
    def __init__(self, name='', cell=None):
        self.applied_to = None
        self.name = name
        self.cell = None

    def apply(self, avatar):
        self.applied_to = avatar
        if self.cell:
            self.cell.pickup = None

    def serialise(self):
        return {'name': self.name}


class MockCell(Cell):
    def __init__(self, location=1, cell_content=Floor({}),
                 avatar=None, pickup=None, name=None, actions=[]):
        self.location = location
        self.cell_content = cell_content
        self.avatar = avatar
        self.pickup = pickup
        self.name = name
        self.actions = actions
        self.partially_fogged = False
        self.remove_from_scene = None
        self.add_to_scene = None

    def __eq__(self, other):
        return self is other


class InfiniteMap(WorldMap):
    def __init__(self):
        self._cell_cache = {}
        [self.get_cell(Location(x, y)) for x in range(5) for y in range(5)]
        self.updates = 0
        self.num_avatars = None
        self.settings = defaultdict(lambda: 0)
        self.infi = 1000

    # Need to override this as self.grid does not exit in the mock object
    def min_x(self): return -self.infi
    def min_y(self): return -self.infi
    def max_x(self): return self.infi
    def max_y(self): return self.infi

    def is_on_map(self, target_location):
        self.get_cell(target_location)
        return True

    def all_cells(self):
        return (cell for cell in self._cell_cache.values())

    def get_cell(self, location):
        return self._cell_cache.setdefault(location, Cell(location))

    def update(self, num_avatars):
        self.updates += 1
        self.num_avatars = num_avatars

    @property
    def num_rows(self):
        return float('inf')

    @property
    def num_cols(self):
        return float('inf')


class EmptyMap(WorldMap):
    def __init__(self):
        pass

    def get_random_spawn_location(self):
        return Location(10, 10)

    def can_move_to(self, target_location):
        return False

    def all_cells(self):
        return iter(())

    def get_cell(self, location):
        return Cell(location)


class ScoreOnOddColumnsMap(InfiniteMap):
    def get_cell(self, location):
        default_cell = Cell(location, generates_score=(location.x % 2 == 1))
        return self._cell_cache.setdefault(location, default_cell)


class AvatarMap(WorldMap):
    def __init__(self, avatar):
        self._avatar = avatar
        self._cell_cache = {}

    def get_cell(self, location):
        if location not in self._cell_cache:
            cell = Cell(location)
            cell.avatar = self._avatar
            self._cell_cache[location] = cell
        return self._cell_cache[location]

    def get_random_spawn_location(self):
        return Location(10, 10)


class PickupMap(WorldMap):
    def __init__(self, pickup):
        self._pickup = pickup

    def get_cell(self, location):
        cell = Cell(location)
        cell.pickup = self._pickup
        return cell
