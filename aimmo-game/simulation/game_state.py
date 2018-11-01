from threading import RLock
from simulation.pickups import serialise_pickups


class GameState(object):
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """

    def __init__(self, world_map, avatar_manager, completion_check_callback=lambda: None):
        self.world_map = world_map
        self.avatar_manager = avatar_manager
        self._completion_callback = completion_check_callback
        self.main_avatar_id = None
        self._lock = RLock()

    def add_avatar(self, player_id, location=None):
        with self._lock:
            location = self.world_map.get_random_spawn_location() if location is None else location
            avatar = self.avatar_manager.add_avatar(player_id, location)
            self.world_map.get_cell(location).avatar = avatar

    def add_avatars(self, player_ids):
        for player_id in player_ids:
            self.add_avatar(player_id)

    def delete_avatars(self, player_ids):
        for player_id in player_ids:
            self.remove_avatar(player_id)

    def remove_avatar(self, player_id):
        with self._lock:
            try:
                avatar = self.avatar_manager.get_avatar(player_id)
            except KeyError:
                return
            self.world_map.get_cell(avatar.location).avatar = None
            self.avatar_manager.remove_avatar(player_id)

    def _update_effects(self):
        with self._lock:
            for avatar in self.avatar_manager.active_avatars:
                avatar.update_effects()

    def update_environment(self):
        with self._lock:
            self._update_effects()
            num_avatars = len(self.avatar_manager.active_avatars)
            self.world_map.update(num_avatars)

    def is_complete(self):
        with self._lock:
            return self._completion_callback(self)

    def get_main_avatar(self):
        with self._lock:
            return self.avatar_manager.avatars_by_id[self.main_avatar_id]

    def serialise(self):
        return {
            'era': "less_flat",
            'southWestCorner': self.world_map.get_serialised_south_west_corner(),
            'northEastCorner': self.world_map.get_serialised_north_east_corner(),
            'players': self.avatar_manager.serialise_players(),
            'pickups': serialise_pickups(self.world_map),
            'scoreLocations': (self.world_map.serialise_score_location()),
            'obstacles': self.world_map.serialise_obstacles()
        }

    def serialise_for_worker(self, avatar_wrapper):
        with self._lock:
            return {
                'avatar_state': avatar_wrapper.serialise(),
                'world_map': {
                    'cells': [cell.serialise() for cell in self.world_map.all_cells()]
                }
            }

    def get_serialised_game_states_for_workers(self):
        with self._lock:
            return {player_id: self.serialise_for_worker(avatar_wrapper) for player_id, avatar_wrapper
                    in self.avatar_manager.avatars_by_id.items()}
