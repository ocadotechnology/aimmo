import random
import math

from simulation.direction import Direction
from simulation.location import Location


class HealthPickup(object):
    def __init__(self, health_restored=3):
        self.health_restored = health_restored

    def __repr__(self):
        return 'HealthPickup(health_restored={})'.format(self.health_restored)


class Cell(object):
    """
    Any position on the world grid.
    """

    def __init__(self, location, habitable=True, generates_score=False, avatar=None, pickup=None):
        self.location = location
        self.habitable = habitable
        self.generates_score = generates_score
        self.avatar = None
        self.pickup = HealthPickup(**pickup) if pickup else None

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={})'.format(self.location, self.habitable, self.generates_score, self.avatar, self.pickup)

    def __eq__(self, other):
        return self.location == other.location


class WorldMap(object):
    """
    The non-player world state.
    """

    def __init__(self, cells):
        self.cells = {}
        for key, cell_data in cells.items():
            location = tuple(key.split(','))
            location_object = Location(x=location[0], y=location[1])
            self.cells[location] = Cell(location=location, **cell_data)

    def all_cells(self):
        return self.cells

    def score_cells(self):
        return (c for c in self.all_cells() if c.generates_score)

    def potential_spawn_locations(self):
        return (c for c in self.all_cells() if c.habitable and not c.generates_score and not c.avatar and not c.pickup)

    def pickup_cells(self):
        return (c for c in self.all_cells() if c.pickup)

    def is_on_map(self, location):
        return (0 <= location.y < self.num_rows) and (0 <= location.x < self.num_cols)

    def get_cell(self, location):
        if not self.is_on_map(location):
            raise ValueError('Location %s is not on the map' % location)
        cell = self.cells[(location.x, location.y)]
        assert cell.location == location, 'location lookup mismatch: arg={}, found={}'.format(location, cell.location)
        return cell

    def can_move_to(self, target_location):
        if not self.is_on_map(target_location):
            return False

        cell = self.get_cell(target_location)
        return cell.habitable and not cell.avatar

    def __repr__(self):
        return repr(self.cells)
