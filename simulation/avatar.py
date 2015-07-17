from simulation.action import MoveAction
from simulation import direction


class AvatarRunner(object):
    def __init__(self, initial_location, initial_code, id):
        self.location = initial_location
        self.events = []
        self.id = id
        self.set_code(initial_code)

    def handle_turn(self, state):
        next_action = self.avatar.handle_turn(state, self.events)

        # Reset event log
        self.events = []

        return next_action

    def add_event(self, event):
        self.events.append(event)

    def set_code(self, code):
        self.code = code
        exec(code)
        self.avatar = Avatar()
