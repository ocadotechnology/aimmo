class Location(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, direction):
        return Location(self.x + direction.x, self.y + direction.y)

    def __repr__(self):
        return 'Location(%d, %d)' % (self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)