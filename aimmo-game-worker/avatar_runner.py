import logging
import traceback
import sys

from six import StringIO

from simulation.action import WaitAction

LOGGER = logging.getLogger(__name__)


class AvatarRunner(object):
    def __init__(self, avatar=None):
        self.avatar = avatar
        self.auto_update = True
        self.avatar_source_code = None

    @staticmethod
    def _get_avatar_src_code():
        with open('avatar.py', 'r') as avatar_file:
            return avatar_file.read()

    def _avatar_src_changed(self):
        new_avatar_code = self._get_avatar_src_code()
        return new_avatar_code != self.avatar_source_code

    def _update_avatar_source_code(self):
        self.avatar_source_code = self._get_avatar_src_code()

    def _update_avatar(self):
        # We import avatar module here because it is not ready at class definition time
        import avatar

        if self.avatar is None:
            # create avatar for the first time
            self.avatar = avatar.Avatar()
            self._update_avatar_source_code()
        elif self.auto_update and self._avatar_src_changed():
            avatar = reload(avatar)
            self.avatar = avatar.Avatar()
            self._update_avatar_source_code()

    def process_avatar_turn(self, world_map, avatar_state):
        output_log = StringIO()

        try:
            sys.stdout = output_log
            sys.stderr = output_log
            self._update_avatar()

            action = self.avatar.handle_turn(world_map, avatar_state)
            action = action.serialise()

        except Exception as e:
            traceback.print_exc()
            LOGGER.error("Code failed to run")
            LOGGER.error(e)
            action = WaitAction().serialise()

        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        logs = output_log.getvalue()
        return action, logs
