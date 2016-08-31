class Location(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __add__(self, direction):
        try:
            d_x = direction.x
            d_y = direction.y
        except AttributeError:
            if direction is None:
                return self
            raise TypeError('Not a direction.')
        else:
            return Location(self.x + d_x, self.y + d_y)

    def __sub__(self, direction):
        return Location(self.x - direction.x, self.y - direction.y)

    def __repr__(self):
        return 'Location({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def serialise(self):
        return {'x': self.x, 'y': self.y}
