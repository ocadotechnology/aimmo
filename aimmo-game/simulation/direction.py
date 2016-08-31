class Direction:
    def __init__(self, x, y):
        if abs(x) not in [0, 1]:
            raise ValueError
        if abs(y) not in [0, 1]:
            raise ValueError
        if abs(x) + abs(y) != 1:
            raise ValueError
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def dict(self):
        return {'x': self.x, 'y': self.y}

    def __repr__(self):
        return 'Direction(x={}, y={})'.format(self.x, self.y)

    @staticmethod
    def from_dict(direction_dict):
        return Direction(**direction_dict)

NORTH = Direction(0, 1)
EAST = Direction(1, 0)
SOUTH = Direction(0, -1)
WEST = Direction(-1, 0)

ALL_DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
