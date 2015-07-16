class _Direction:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

NORTH = _Direction(0, 1)
EAST = _Direction(1, 0)
SOUTH = _Direction(0, -1)
WEST = _Direction(-1, 0)
