import traceback
import sys

from simulation.action import WaitAction


# This class will be implemented by the player
Avatar = None


class UserCodeException(Exception):
    def to_user_string(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        a = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return a


class AvatarWrapper(object):
    def __init__(self, initial_location, initial_code, player_id):
        self.location = initial_location
        self.health = 5
        self.score = 0
        self.events = []
        self.player_id = player_id
        self.avatar = None
        self.last_move = None
        self.set_code(initial_code)

    def handle_turn(self, state):
        try:
            next_action = self.avatar.handle_turn(state, self.events)
        except Exception as e:
            # TODO: tell user their program threw an exception during execution somehow...
            print('avatar threw exception during handle_turn:', e)
            traceback.print_exc()
            next_action = WaitAction()
        # Reset event log
        self.events = []
        if next_action.direction:
            self.last_move = next_action.direction

        return next_action

    def die(self, respawn_location):
        # TODO: extract settings for health and score loss on death
        self.health = 5
        self.score = max(0, self.score - 2)
        self.location = respawn_location

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
        return 'Avatar(id={}, location={}, health={}, score={}, last_move={})'.format(
            self.player_id,
            self.location,
           self.health,
           self.score,
           self.last_move)

