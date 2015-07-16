class WorldState(object):
    def __init__(self, world_map, player_manager):
        self.world_map = world_map
        self.player_manager = player_manager

    def get_state_for(self, player):
        return self

    def get_players_at(self, location):
        return [p for p in self.player_manager.players if p.location == location]
