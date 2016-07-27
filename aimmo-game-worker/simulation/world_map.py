from simulation.location import Location

from simulation.avatar_state import AvatarState


class HealthPickup(object):

    def __init__(self, health_restored=3):
        self.health_restored = health_restored

    def __repr__(self):
        return 'HealthPickup(health_restored={})'.format(self.health_restored)


class Cell(object):

    """
    Any position on the world grid.
    """

    def __init__(self, location, generates_score, habitable=None, avatar=None, pickup=None, partially_fogged=True):
        self.location = Location(**location)
        self.generates_score = generates_score
        self.partially_fogged = partially_fogged
        if not partially_fogged:
            self.habitable = habitable
            self.avatar = AvatarState(**avatar) if avatar else None
            self.pickup = HealthPickup(**pickup) if pickup else None

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={} f={})'.format(self.location, getattr(self, 'habitable', 0), self.generates_score, getattr(self, 'avatar', 0), getattr(self, 'pickup', 0), self.partially_fogged)

    def __eq__(self, other):
        return self.location == other.location


class WorldMap(object):

    """
    The non-player world state.
    """

    def __init__(self, cells):
        self.cells = {}
        for cell_data in cells:
            cell = Cell(**cell_data)
            self.cells[cell.location] = cell

    def all_cells(self):
        return self.cells.values()

    def score_cells(self):
        return (c for c in self.all_cells() if c.generates_score)

    def pickup_cells(self):
        return (c for c in self.all_cells() if getattr(self, 'pickup', False))

    def partially_fogged_cells(self):
        return (c for c in self.all_cells() if c.partially_fogged)

    def is_on_map(self, location):
        return location in self.cells

    def get_cell(self, location):
        cell = self.cells[location]
        assert cell.location == location, 'location lookup mismatch: arg={}, found={}'.format(
            location, cell.location)
        return cell

    def can_move_to(self, target_location):
        try:
            cell = self.get_cell(target_location)
        except KeyError:
            return False
        return getattr(cell, 'habitable', False) and not getattr(cell, 'avatar', False)

    def __repr__(self):
        return repr(self.cells)
