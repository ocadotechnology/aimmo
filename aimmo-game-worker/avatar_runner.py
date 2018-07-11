import logging
from simulation.action import WaitAction

LOGGER = logging.getLogger(__name__)

class AvatarRunner:
    def    __init__(self, avatar=None):
        if avatar is None:
            from avatar import Avatar
            self.avatar = Avatar()
        else:
            self.avatar = avatar
    
    def handle_turn(self, world_map, avatar_state):
        try:
            return self.avatar.handle_turn(avatar_state, world_map)
        except Exception as e:
            LOGGER.error("Code failed to run")
            LOGGER.error(e)
            action = WaitAction()
        return action
