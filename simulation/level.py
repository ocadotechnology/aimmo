import random

class Level:

    def generate_special_square_and_return_coords(self, special_square_map, special_square_list, limit):
        while len(special_square_list) < limit:
            new_coords = self.empty_squares.pop([random.randint(0, len(self.empty_squares))])
            special_square_list.append(new_coords)
            special_square_map[new_coords] = SpecialSquare(random.randint(1,5))

    def generate_scoring_squares(self, limit):
        self.generate_special_square_and_return_coords(self.coords_of_scoring_squares, self.scoring_squares, limit)

    def generate_health_squares(self, limit):
        self.generate_special_square_and_return_coords(self.coords_of_health_squares, self.health_squares, limit)

    def generate_attack_squares(self, limit):
        self.generate_special_square_and_return_coords(self.coords_of_attack_squares, self.attack_squares, limit)

    def __init__(self, height, width, number_of_obstacle_squares, number_of_scoring_squares, number_of_health_squares, number_of_attack_squares):
        def verify_enough_space_for_specified_squares():
            total_number_of_special_squares = number_of_obstacle_squares + number_of_scoring_squares + number_of_health_squares + number_of_attack_squares
            if total_number_of_special_squares > height * width:
                raise Exception("The Level isn't big enough for " + total_number_of_special_squares + " special squares")

        def generate_list_of_empty_squares():
            list_of_empty_squares = []
            for x in range(0, width):
                for y in range(0, height):
                    list_of_empty_squares.add({x,y})
            return list_of_empty_squares

        def generate_obstacle_squares(limit):
            while len(self.coords_of_obstacle_squares) < limit:
                self.coords_of_obstacle_squares.add(self.empty_squares.pop([random.randint(0, len(self.empty_squares))]))

        def initialise_special_squares():
            generate_obstacle_squares(number_of_obstacle_squares)
            self.generate_scoring_squares(number_of_scoring_squares)
            self.generate_health_squares(number_of_health_squares)
            self.generate_attack_squares(number_of_attack_squares)

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
        self.matrix_of_level = [width][height]
        verify_enough_space_for_specified_squares()
        initialise_special_squares()

    def get_and_remove(self, special_square_map, tuple):
        value = special_square_map[tuple]
        del special_square_map[tuple]
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
            return "score"
        if tuple in self.coords_of_attack_squares:
            return "attack"
        if tuple in self.coords_of_health_squares:
            return "health"
        if tuple in self.coords_of_obstacle_squares:
            return "obstacle"

# TODO: can split/extend it into specific score, attack and health squares but they can be covered with this as they are
class SpecialSquare:

    def __init__(self, points_per_turn):
        self.value = points_per_turn
