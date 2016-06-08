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
        return {
            'avatar_state': avatar_wrapper.serialise(),
            'world_map': {
                'cells': [cell.serialise() for cell in processed_world_map.all_cells()]
            }
        }
        return WorldView(avatar_wrapper, processed_world_map, self.avatar_manager)

    def add_avatar(self, user_id, worker_url):
        spawn_location = self.world_map.get_random_spawn_location()
        avatar = self.avatar_manager.add_avatar(user_id, worker_url, spawn_location)
        self.world_map.get_cell(spawn_location).avatar = avatar

    def remove_avatar(self, user_id):
        try:
            avatar = self.avatar_manager.avatarsById[user_id]
        except KeyError:
            return
        self.world_map.get_cell(avatar.location).avatar = None
        self.avatar_manager.remove_avatar(user_id)
