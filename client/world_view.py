class WorldView(object):
    def __init__(self, avatar_state, terrain_view, avatar_manager):
        self.avatar_state = avatar_state
        self.world_view = terrain_view
        self.avatar_manager = avatar_manager
