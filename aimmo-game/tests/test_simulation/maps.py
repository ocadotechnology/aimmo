

from collections import defaultdict

from simulation.cell import Cell
from simulation.game_logic import SpawnLocationFinder
from simulation.interactables.score_location import ScoreLocation
from simulation.location import Location
from simulation.world_map import WorldMap


class MockPickup(object):
    def __init__(self, name='', cell=None, target=None):
        self.applied_to = target
        self.name = name
        self.cell = None

    def apply(self):
        if self.cell:
            self.cell.interactable = None

    def conditions_met(self, world_map):
        return True

    def serialize(self):
        return {'name': self.name}


class MockCell(Cell):
    def __init__(self, location=Location(0, 0), habitable=True,
                 avatar=None, interactable=None, name=None, actions=[]):
        self.location = location
        self.habitable = habitable
        self.avatar = avatar
        self.interactable = interactable
        self.name = name
        self.actions = actions
        self.partially_fogged = False

    def __eq__(self, other):
        return self is other


class InfiniteMap(WorldMap):
    def __init__(self):
        self._spawn_location_finder = SpawnLocationFinder(self)
        self._cell_cache = {}
        [self.get_cell(Location(x, y)) for x in range(5) for y in range(5)]
        self.updates = 0
        self.num_avatars = None
        self.settings = defaultdict(lambda: 0)

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
        default_cell = Cell(location)
        if location.x % 2 == 1:
            default_cell.interactable = ScoreLocation(default_cell)
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
        cell.interactable = self._pickup
        return cell
