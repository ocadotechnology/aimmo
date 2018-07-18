import logging
import traceback
from simulation.action import WaitAction

LOGGER = logging.getLogger(__name__)


class AvatarRunner(object):
    def __init__(self, avatar=None):
        self.avatar = avatar

    def process_avatar_turn(self, world_map, avatar_state):
        try:
            if self.avatar is None:
                from avatar import Avatar
                self.avatar = Avatar()
            return self.avatar.handle_turn(world_map, avatar_state)

        except Exception as e:
            LOGGER.error("Code failed to run")
            LOGGER.error(traceback.print_exc())
            action = WaitAction()

        return action
