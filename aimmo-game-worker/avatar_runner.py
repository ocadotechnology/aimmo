import logging
import traceback
import sys
import imp

from six import StringIO

from simulation.action import WaitAction, Action
from user_exceptions import InvalidActionException

LOGGER = logging.getLogger(__name__)


class AvatarRunner(object):
    def __init__(self, avatar=None, auto_update=True):
        self.avatar = avatar
        self.auto_update = auto_update
        self.avatar_source_code = None

    def _avatar_src_changed(self, new_avatar_code):
        return new_avatar_code != self.avatar_source_code

    @staticmethod
    def _get_new_avatar(src_code):
        module = imp.new_module('avatar')  # Create a temporary module to execute the src_code in
        exec src_code in module.__dict__
        return module.Avatar()

    def _update_avatar(self, src_code):
        """ If the avatar source code has changed or we have not created an avatar yet,
            we 'import' src_code, and assign self.avatar to a fresh avatar object. """

        if self.avatar is None or self.auto_update and self._avatar_src_changed(src_code):
            self.avatar = self._get_new_avatar(src_code)
            self.avatar_source_code = src_code

    def process_avatar_turn(self, world_map, avatar_state, src_code):
        output_log = StringIO()
        avatar_updated = self._avatar_src_changed(src_code)

        try:
            sys.stdout = output_log
            sys.stderr = output_log
            self._update_avatar(src_code)

            action = self.decide_action(world_map, avatar_state)

        except Exception as e:
            traceback.print_exc()
            LOGGER.info("Code failed to run")
            LOGGER.info(e)
            action = WaitAction().serialise()

        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        logs = output_log.getvalue()
        return {'action': action, 'log': logs, 'avatar_updated': avatar_updated}

    def decide_action(self, world_map, avatar_state):
        action = self.avatar.handle_turn(world_map, avatar_state)
        LOGGER.error(action)
        if not isinstance(action, Action):
            raise InvalidActionException(action)
        return action.serialise()
