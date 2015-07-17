class WorldState(object):
    def __init__(self, world_map, avatar_manager):
        self.world_map = world_map
        self.avatar_manager = avatar_manager

    def get_state_for(self, avatar):
        return self

    def get_avatars_at(self, location):
        return [p for p in self.avatar_manager.avatars
                if p.location == location]
