class WorldState(object):
    def __init__(self, world_map):
        self.world_map = world_map

    def get_state_for(self, player):
        return self
