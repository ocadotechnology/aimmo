import hashlib

class CellTransform():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def compute_id(self):
        return hash(str(self.x) + ":" + str(self.y))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
