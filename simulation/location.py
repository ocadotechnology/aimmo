class Location(object):
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def __add__(self, direction):
        return Location(self.row + direction.row, self.col + direction.col)

    def __sub__(self, direction):
        return Location(self.row - direction.row, self.col - direction.col)

    def __repr__(self):
        return 'Location(row=%d, col=%d)' % (self.row, self.col)

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)
