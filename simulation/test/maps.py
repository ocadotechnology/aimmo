from simulation.world_map import EMPTY, SCORE


class InfiniteMap(object):
    def can_move_to(self, target_location):
        return True

    def get_square(self, location):
        return EMPTY


class EmptyMap(object):
    def can_move_to(self, target_location):
        return False

    def get_square(self, location):
        raise ValueError('EmptyMap has no valid locations')


class ScoreOnOddColumnsMap(InfiniteMap):
    def get_square(self, location):
        if location.col % 2 == 0:
            return EMPTY
        else:
            return SCORE
