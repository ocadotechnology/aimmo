from client.world_view import WorldView
from simulation.avatar import fog_of_war


class GameState(object):
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """

    def __init__(self, world_map, avatar_manager):
        self.world_map = world_map
        self.avatar_manager = avatar_manager

    def get_state_for(self, avatar_wrapper):
        processed_world_map = fog_of_war.apply_fog_of_war(self.world_map, avatar_wrapper)
        return WorldView(avatar_wrapper, processed_world_map, self.avatar_manager)

    def player_changed_code(self, player_id, code):
        avatar = self.avatar_manager.avatarsById.get(player_id)
        if avatar:
            avatar.set_code(code)
        else:
            spawn_location = self.world_map.get_random_spawn_location()
            avatar = self.avatar_manager.spawn(player_id, code, spawn_location)
            self.world_map.get_cell(spawn_location).avatar = avatar
