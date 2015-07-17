import random

class Level:
    def __init__(self, height, width, obstacle_ratio, scoring_square_ratio):
        self.matrix_of_level = [[None for _ in xrange(width)] for _ in xrange(height)]

        for y in xrange(height):
            for x in xrange(width):
                if random.random() < obstacle_ratio:
                    self.matrix_of_level[y][x] = OBSTACLE
                elif random.random() < scoring_square_ratio:
                    self.matrix_of_level[y][x] = SCORE
                else:
                    self.matrix_of_level[y][x] = EMPTY

        print [[x.key for x in y] for y in self.matrix_of_level]

class SquareType:
    def __init__(self, name, key):
        self.name = name
        self.key = key

EMPTY = SquareType("empty", 0)
OBSTACLE = SquareType("obstacle", 1)
SCORE = SquareType("score", 2)
