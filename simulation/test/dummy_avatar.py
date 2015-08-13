from simulation.action import MoveAction
from simulation import direction


class DummyAvatarRunner(object):
    def __init__(self, initial_location, player_id):
        self.health = 5
        self.location = initial_location
        self.player_id = player_id
        self.events = []

    def handle_turn(self, state):
        next_action = MoveAction(direction.EAST)

        # Reset event log
        self.events = []

        return next_action

    def add_event(self, event):
        self.events.append(event)
