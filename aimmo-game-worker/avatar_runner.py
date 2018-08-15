import logging
import traceback
import sys
import inspect

from six import StringIO

from simulation.action import WaitAction

LOGGER = logging.getLogger(__name__)


class AvatarRunner(object):
    def __init__(self, avatar=None):
        self.avatar = avatar
        self.auto_update = True
        self.avatar_source_code = None

    def _avatar_src_changed(self):
        import avatar  # We import avatar here because the module isn't ready at class definition time
        reload(avatar)
        LOGGER.info('Reloaded avatar source: {}'.format(inspect.getsource(avatar.Avatar)))
        return inspect.getsource(avatar.Avatar) != self.avatar_source_code

    def _update_avatar(self):
        import avatar

        if self.avatar is None:
            # Load and create avatar for the first time
            self.avatar = avatar.Avatar()
            self.avatar_source_code = inspect.getsource(avatar.Avatar)
        elif self.auto_update and self._avatar_src_changed():
            reload(avatar)
            self.avatar = avatar.Avatar()
            LOGGER.info('Making new avatar')
            self.avatar_source_code = inspect.getsource(avatar.Avatar)

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
