from __future__ import absolute_import
from simulation import world_map
from simulation.location import Location
from simulation.world_map import Cell


class MockCell(Cell):
    def __init__(self, location=1, habitable=True, generates_score=False,
                 avatar=None, pickup=None, name=None):
        self.location = location
        self.habitable = habitable
        self.generates_score = generates_score
        self.avatar = avatar
        self.pickup = pickup
        self.name = name

    def __eq__(self, other):
        return self is other


class InfiniteMap(world_map.WorldMap):
    def __init__(self):
        pass

    def can_move_to(self, target_location):
        return True

    def all_cells(self):
        yield world_map.Cell(Location(0, 0))

    def get_cell(self, location):
        return world_map.Cell(location)


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
        if location.x % 2 == 0:
            return world_map.Cell(location)
        else:
            return world_map.Cell(location, habitable=True, generates_score=True)


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
