# TODO: investigate using x and y
class Direction:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return 'Direction(x={}, y={})'.format(self.x, self.y)

NORTH = Direction(0, 1, 'north')
EAST = Direction(1, 0, 'east')
SOUTH = Direction(0, -1, 'south')
WEST = Direction(-1, 0, 'west')

ALL_DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
