from __future__ import absolute_import
from simulation import world_map
from simulation.location import Location
from simulation.world_map import Cell


class MockCell(Cell):
    def __init__(self, location=1, habitable=True, generates_score=False,
                 avatar=None, pickup=None, name=None, actions=[]):
        self.location = location
        self.habitable = habitable
        self.generates_score = generates_score
        self.avatar = avatar
        self.pickup = pickup
        self.name = name
        self.actions = actions

    def __eq__(self, other):
        return self is other


class InfiniteMap(world_map.WorldMap):
    def __init__(self):
        self._cell_cache = {}
        [self.get_cell(Location(x, y)) for x in range(5) for y in range(5)]

    def is_on_map(self, target_location):
        self.get_cell(target_location)
        return True

    def all_cells(self):
        return (cell for cell in self._cell_cache.values())

    def get_cell(self, location):
        return self._cell_cache.setdefault(location, Cell(location))


class EmptyMap(world_map.WorldMap):
    def __init__(self):
        pass

    def can_move_to(self, target_location):
        return False

    def all_cells(self):
        return iter(())

    def get_cell(self, location):
        return world_map.Cell(location)


class ScoreOnOddColumnsMap(InfiniteMap):
    def get_cell(self, location):
        default_cell = Cell(location, generates_score=(location.x % 2 == 1))
        return self._cell_cache.setdefault(location, default_cell)


class AvatarMap(world_map.WorldMap):
    def __init__(self, avatar):
        self._avatar = avatar
        self._cell_cache = {}

    def get_cell(self, location):
        if location not in self._cell_cache:
            cell = world_map.Cell(location)
            cell.avatar = self._avatar
            self._cell_cache[location] = cell
        return self._cell_cache[location]

    def get_random_spawn_location(self):
        return Location(10, 10)
