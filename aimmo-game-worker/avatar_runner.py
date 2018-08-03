import logging
import traceback
import sys

from six import StringIO

from simulation.action import WaitAction


LOGGER = logging.getLogger(__name__)


class AvatarRunner(object):
    def __init__(self, avatar=None):
        self.avatar = avatar

    def process_avatar_turn(self, world_map, avatar_state):
        output_log = StringIO()

        try:
            sys.stdout = output_log
            sys.stderr = output_log
            if self.avatar is None:
                from avatar import Avatar
                self.avatar = Avatar()

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
