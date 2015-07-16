from simulation.action import MoveAction
from simulation import direction


class DummyPlayer(object):
    def __init__(self, initial_location):
        self.location = initial_location

    def handle_turn(self, state):
        return MoveAction(direction.EAST)
