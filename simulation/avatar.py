from simulation.action import MoveAction
from simulation import direction


class AvatarRunner(object):
    def __init__(self, initial_location, initial_code, id, avatar_appearance):
        self.location = initial_location
        self.events = []
        self.id = id
        self.set_code(initial_code)
        self.avatar_appearance = avatar_appearance

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

class AvatarAppearance:
    def __init__(self, body_stroke, body_fill, eye_stroke, eye_fill):
        self.body_stroke = body_stroke
        self.body_fill = body_fill
        self.eye_stroke = eye_stroke
        self.eye_fill = eye_fill

