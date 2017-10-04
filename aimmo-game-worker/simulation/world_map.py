from geography.cell import Cell


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
