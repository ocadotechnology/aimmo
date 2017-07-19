class CellTransform():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    # TODO: change to hash lib
    def compute_id(self):
        return int(bin(self.x * 666013) ^ bin(self.y * 10007))

    def get_x(self):
        return x

    def get_y(self):
        return y
