class Direction:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

NORTH = Direction(-1, 0)
EAST = Direction(0, 1)
SOUTH = Direction(1, 0)
WEST = Direction(0, -1)
