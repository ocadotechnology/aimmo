class Direction(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Direction(x={}, y={})'.format(self.x, self.y)

    def serialise(self):
        return {
            'x': self.x,
            'y': self.y,
        }

NORTH = Direction(0, 1)
EAST = Direction(1, 0)
SOUTH = Direction(0, -1)
WEST = Direction(-1, 0)

ALL_DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
