from simulation.action import MoveAction
from simulation import direction


class DummyPlayer(object):
    def __init__(self, initial_location):
        self.location = initial_location
        self.events = []

    def handle_turn(self, state):
        # TODO pass events to player
        # TODO delegate action generation to player

        # Reset event log
        self.events = []

        return MoveAction(direction.EAST)

    def add_event(self, event):
        self.events.append(event)
