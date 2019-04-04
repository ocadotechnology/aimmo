from .avatar_state import AvatarState
from .location import Location


class Cell(object):

    """
    Any position on the world grid.
    """

    def __init__(self, location, avatar=None, **kwargs):
        self.location = Location(**location)
        self.avatar = None
        if avatar:
            self.avatar = AvatarState(
                location=avatar["location"],
                score=avatar["score"],
                health=avatar["health"],
            )
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return "Cell({} h={} a={} i={})".format(
            self.location, self.habitable, self.avatar, self.interactable
        )

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

    def interactable_cells(self):
        return [cell for cells in self.all_cells() if cell.interactable]

    def pickup_cells(self):
        return [
            cell
            for cells in self.interactable_cells
            if "damage_boost" in cell.interactable.values()
            or "invulnerability" in c.interactable.values()
            or "health" in c.interactable.values()
        ]

    def score_cells(self):
        return [
            cell
            for cells in self.interactable_cells()
            if "score" in cell.interactable.values()
        ]

    def partially_fogged_cells(self):
        return [cell for cells in self.all_cells() if cell.partially_fogged]

    def is_visible(self, location):
        return location in self.cells

    def get_cell(self, location):
        cell = self.cells[location]
        assert (
            cell.location == location
        ), "location lookup mismatch: arg={}, found={}".format(location, cell.location)
        return cell

    def can_move_to(self, target_location):
        try:
            cell = self.get_cell(target_location)
        except KeyError:
            return False
        return getattr(cell, "habitable", False) and not getattr(cell, "avatar", False)

    def __repr__(self):
        return repr(self.cells)
