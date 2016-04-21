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

    def __init__(self, location, habitable, generates_score, avatar, pickup):
        self.location = Location(**location)
        self.habitable = habitable
        self.generates_score = generates_score
        self.avatar = AvatarState(**avatar) if avatar else None
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
        for cell_data in cells:
            cell = Cell(**cell_data)
            self.cells[cell.location] = cell

    def all_cells(self):
        return self.cells.values()

    def score_cells(self):
        return (c for c in self.all_cells() if c.generates_score)

    def pickup_cells(self):
        return (c for c in self.all_cells() if c.pickup)

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
        return cell.habitable and not cell.avatar

    def __repr__(self):
        return repr(self.cells)
