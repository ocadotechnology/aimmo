class GameState(object):
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """

    def __init__(self, world_map, avatar_manager, completion_check_callback=lambda: None):
        self.world_map = world_map
        self.avatar_manager = avatar_manager
        self._completion_callback = completion_check_callback
        self.main_avatar_id = None

    def get_state_for(self, avatar_wrapper):
        return {
            'avatar_state': avatar_wrapper.serialise(),
            'world_map': {
                'cells': [cell.serialise() for cell in self.world_map.all_cells()]
            }
        }

    def add_avatar(self, user_id, worker_url, location=None):
        location = self.world_map.get_random_spawn_location() if location is None else location
        avatar = self.avatar_manager.add_avatar(user_id, worker_url, location)
        self.world_map.get_cell(location).avatar = avatar

    def remove_avatar(self, user_id):
        try:
            avatar = self.avatar_manager.get_avatar(user_id)
        except KeyError:
            return
        self.world_map.get_cell(avatar.location).avatar = None
        self.avatar_manager.remove_avatar(user_id)

    def _update_effects(self):
        for avatar in self.avatar_manager.active_avatars:
            avatar.update_effects()

    def update_environment(self):
        self._update_effects()
        num_avatars = len(self.avatar_manager.active_avatars)
        self.world_map.update(num_avatars)

    def is_complete(self):
        return self._completion_callback(self)

    def get_main_avatar(self):
        return self.avatar_manager.avatars_by_id[self.main_avatar_id]
