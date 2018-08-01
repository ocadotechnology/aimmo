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

    def process_avatar_turn(self, world_map, avatar_state):
        import avatar

        output_log = StringIO()

        try:
            sys.stdout = output_log
            sys.stderr = output_log

            if self.avatar is None:
                self.avatar = avatar.Avatar()
            else:
                reload(avatar)
                self.avatar = avatar.Avatar()

            LOGGER.info('Source code: ')
            LOGGER.info(inspect.getsource(avatar.Avatar))

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
