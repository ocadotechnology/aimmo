class Direction:
    def __init__(self, x, y):
        if abs(x) not in [0, 1]:
            raise ValueError
        if abs(y) not in [0, 1]:
            raise ValueError
        if abs(x) + abs(y) != 1:
            raise ValueError
        self.x = x
        self.y = y

    @property
    def dict(self):
        return {'x': self.x, 'y': self.y}

    def __repr__(self):
        return 'Direction(x={}, y={})'.format(self.x, self.y)


NORTH = Direction(0, 1)
EAST = Direction(1, 0)
SOUTH = Direction(0, -1)
WEST = Direction(-1, 0)

ALL_DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
