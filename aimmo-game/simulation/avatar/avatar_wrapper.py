import traceback
import sys

from simulation.action import WaitAction


# This class will be implemented by the player
Avatar = None


class UserCodeException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
        self.exc_type, self.exc_value, self.exc_traceback = sys.exc_info()

    def to_user_string(self):
        lines = traceback.format_exception(self.exc_type, self.exc_value, self.exc_traceback)
        return '<br/>'.join(lines)


class AvatarWrapper(object):
    """
    The application's view of a character, not to be confused with "Avatar", the player-supplied code.
    """

    def __init__(self, initial_location, initial_code, player_id, avatar_appearance):
        self.location = initial_location
        self.health = 5
        self.score = 0
        self.events = []
        self.player_id = player_id
        self.avatar_appearance = avatar_appearance
        self.avatar = None

        self.code = ''
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

        return next_action

    def die(self, respawn_location):
        # TODO: extract settings for health and score loss on death
        self.health = 5
        self.score = max(0, self.score - 2)
        self.location = respawn_location

    def add_event(self, event):
        self.events.append(event)

    def set_code(self, code):
        if self.code != code:
            self.code = code
            try:
                exec(code)
                if Avatar is None:
                    raise Exception('You need to define the class "Avatar"')
                self.avatar = Avatar()
            except Exception as ex:
                raise UserCodeException("Exception in user code", ex)

    def __repr__(self):
        return 'Avatar(id={}, location={}, health={}, score={})'.format(self.player_id, self.location,
                                                                        self.health, self.score)
