import traceback
import sys
from action import WaitAction
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
        self.health = 10
        self.events = []
        self.player_id = player_id
        self.set_code(initial_code)
        self.avatar_appearance = avatar_appearance
        self.avatar = None

    def handle_turn(self, state):
        try:
            next_action = self.avatar.handle_turn(state, self.events)
        except Exception as e:
            # TODO: tell user their program threw an exception during execution somehow...
            print 'avatar threw exception during handle_turn:', e
            traceback.print_exc()
            next_action = WaitAction()
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

    def __repr__(self):
        return 'Avatar(id={}, location={}, health={})'.format(self.player_id, self.location, self.health)


class AvatarAppearance:
    def __init__(self, body_stroke, body_fill, eye_stroke, eye_fill):
        self.body_stroke = body_stroke
        self.body_fill = body_fill
        self.eye_stroke = eye_stroke
        self.eye_fill = eye_fill
