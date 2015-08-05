import traceback
import sys
from simulation.action import MoveAction
from simulation import direction


# This class will be implemented by the player
Avatar = None


class UserCodeException(Exception):
    def to_user_string(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return '<br/>'.join(lines)


class AvatarRunner(object):
    def __init__(self, initial_location, initial_code, player_id, avatar_appearance):
        self.location = initial_location
        self.events = []
        self.player_id = player_id
        self.set_code(initial_code)
        self.avatar_appearance = avatar_appearance
        self.avatar = None

    def handle_turn(self, state):
        next_action = self.avatar.handle_turn(state, self.events)

        # Reset event log
        self.events = []

        return next_action

    def add_event(self, event):
        self.events.append(event)

    def set_code(self, code):
        self.code = code
        try:
            exec(code)
        except Exception as ex:
            raise UserCodeException("Exception in user code", ex)
        self.avatar = Avatar()


class AvatarAppearance:
    def __init__(self, body_stroke, body_fill, eye_stroke, eye_fill):
        self.body_stroke = body_stroke
        self.body_fill = body_fill
        self.eye_stroke = eye_stroke
        self.eye_fill = eye_fill
