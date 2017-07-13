from .avatar_state import AvatarState
from .location import Location


class Cell(object):

    """
    Any position on the world grid.
    """

    def __init__(self, location, avatar=None, **kwargs):
        self.location = Location(**location)
        if avatar:
            self.avatar = AvatarState(**avatar)
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={})'.format(
            self.location,
            getattr(self, 'habitable', 0),
            self.generates_score,
            getattr(self, 'avatar', 0),
            getattr(self, 'pickup', 0))

    def __eq__(self, other):
        return self.location == other.location

    def __ne__(self, other):
        return not self == other


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
        return (c for c in self.all_cells() if getattr(c, 'pickup', False))

    def partially_fogged_cells(self):
        return (c for c in self.all_cells() if c.partially_fogged)

    def is_visible(self, location):
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
