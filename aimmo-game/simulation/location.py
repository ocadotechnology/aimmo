class Location(object):
    def __init__(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Location needs to be an integer!")

        self.x = x
        self.y = y

    def __add__(self, direction):
        return Location(self.x + direction.x, self.y + direction.y)

    def __sub__(self, direction):
        return Location(self.x - direction.x, self.y - direction.y)

    def __repr__(self):
        return "Location({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y))

    def serialize(self):
        return {"x": self.x, "y": self.y}
