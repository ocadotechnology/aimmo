# TODO: investigate using x and y
class Direction:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return self.name

NORTH = Direction(0, 1, "EAST")
EAST = Direction(1, 0, "EAST")
SOUTH = Direction(0, -1, "SOUTH")
WEST = Direction(-1, 0, "WEST")

ALL_DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
