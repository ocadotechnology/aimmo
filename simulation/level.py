import random

# TODO: introduce enum (equivalent) for what type of square it is and use that for calculating stuffs
class Level:

    def remove_all_scoring_squares(self):
        for t in self.scoring_squares:
            self.coords_of_scoring_squares.remove(t)
            self.empty_squares.append(t)
            del self.scoring_squares[t]

    def regenerate_initial_number_of_scoring_squares(self):
        self.remove_all_scoring_squares()
        self.generate_scoring_squares(self.initial_number_of_scoring_squares)

    def generate_special_square_and_return_coords(self, special_square_list, special_square_map, limit, type):
        while len(special_square_list) < limit:
            new_coords = tuple(self.empty_squares.pop(random.randint(0, len(self.empty_squares))))
            special_square_list.append(new_coords)
            special_square_map[new_coords] = SpecialSquare(random.randint(1, 5))
        for c in range(special_square_list):
            self.matrix_of_level[c[0]][c[1]] = type

    def generate_scoring_squares(self, limit):
        self.generate_special_square_and_return_coords(self.coords_of_scoring_squares, self.scoring_squares, limit, SCORE)

    def generate_health_squares(self, limit):
        self.generate_special_square_and_return_coords(self.coords_of_health_squares, self.health_squares, limit, HEALTH)

    def generate_attack_squares(self, limit):
        self.generate_special_square_and_return_coords(self.coords_of_attack_squares, self.attack_squares, limit, ATTACK)

    def __init__(self, height, width, number_of_obstacle_squares, number_of_scoring_squares, number_of_health_squares, number_of_attack_squares):
        def verify_enough_space_for_specified_squares():
            total_number_of_special_squares = number_of_obstacle_squares + number_of_scoring_squares + number_of_health_squares + number_of_attack_squares
            if total_number_of_special_squares > height * width:
                raise Exception("The Level isn't big enough for " + total_number_of_special_squares + " special squares")

        def generate_list_of_empty_squares():
            list_of_empty_squares = []
            for x in range(0, width):
                for y in range(0, height):
                    list_of_empty_squares.append({x,y})
            return list_of_empty_squares

        def generate_obstacle_squares(limit):
            while len(self.coords_of_obstacle_squares) < limit:
                self.coords_of_obstacle_squares.append(self.empty_squares.pop(random.randint(0, len(self.empty_squares))))
            for c in range(self.coords_of_obstacle_squares):
                self.matrix_of_level[c[0]][c[1]] = OBSTACLE

        def initialise_special_squares():
            generate_obstacle_squares(number_of_obstacle_squares)
            self.generate_scoring_squares(number_of_scoring_squares)
            self.generate_health_squares(number_of_health_squares)
            self.generate_attack_squares(number_of_attack_squares)

        self.initial_number_of_scoring_squares = number_of_scoring_squares
        # coordinates of special squares
        self.coords_of_obstacle_squares = []
        self.coords_of_scoring_squares = []
        self.coords_of_health_squares = []
        self.coords_of_attack_squares = []
        # Map coords to Squares with values
        self.scoring_squares = {}
        self.health_squares = {}
        self.attack_squares = {}
        self.empty_squares = generate_list_of_empty_squares()
        self.matrix_of_level = [[EMPTY for _ in xrange(width)] for _ in xrange(height)]

        verify_enough_space_for_specified_squares()
        initialise_special_squares()

    def get_and_remove(self, special_square_map, tuple):
        value = special_square_map[tuple]
        del special_square_map[tuple]
        self.empty_squares.append(tuple)
        return value

    def get_score(self, tuple):
        if tuple in self.coords_of_scoring_squares:
            return self.scoring_squares[tuple].value
        return 0

    def get_health_if_it_exists(self, tuple):
        return self.get_and_remove(self.health_squares, tuple)

    def get_attack_if_it_exists(self, tuple):
        return self.get_and_remove(self.attack_squares, tuple)

    # TODO: can return types rather than just strings
    def get_type(self, tuple):
        if tuple in self.coords_of_scoring_squares:
            return SCORE
        if tuple in self.coords_of_attack_squares:
            return ATTACK
        if tuple in self.coords_of_health_squares:
            return HEALTH
        if tuple in self.coords_of_obstacle_squares:
            return OBSTACLE
        return EMPTY

class SquareType:

    def __init__(self, name, key):
        self.name = name
        self.key = key

EMPTY = SquareType("empty", 0)
OBSTACLE = SquareType("obstacle", 1)
SCORE = SquareType("score", 2)
ATTACK = SquareType("attack", 3)
HEALTH = SquareType("health", 4)

# TODO: can split/extend it into specific score, attack and health squares but they can be covered with this as they are
class SpecialSquare:

    def __init__(self, points_per_turn):
        self.value = points_per_turn
