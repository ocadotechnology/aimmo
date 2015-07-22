import random
import numpy as np


class Level:
    def __init__(self, height, width, obstacle_ratio, scoring_square_ratio):
        self.matrix_of_level = np.empty((height, width), dtype=object)

        for y in xrange(height):
            for x in xrange(width):
                if random.random() < obstacle_ratio:
                    self.matrix_of_level[y, x] = OBSTACLE
                elif random.random() < scoring_square_ratio:
                    self.matrix_of_level[y, x] = SCORE
                else:
                    self.matrix_of_level[y, x] = EMPTY


class SquareType:
    def __init__(self, name, key):
        self.name = name
        self.key = key

EMPTY = SquareType("empty", 0)
OBSTACLE = SquareType("obstacle", 1)
SCORE = SquareType("score", 2)
