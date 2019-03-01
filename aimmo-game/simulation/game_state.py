from threading import RLock

from simulation.pickups.pickup_types import serialize_pickups


class GameState:
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """

    def __init__(self, world_map, avatar_manager, completion_check_callback=lambda: None):
        self.world_map = world_map
        self.avatar_manager = avatar_manager
        self.main_avatar_id = None
        self._lock = RLock()

    def get_main_avatar(self):
        with self._lock:
            return self.avatar_manager.avatars_by_id[self.main_avatar_id]

    def serialise(self):
        return {
            'era': "less_flat",
            'southWestCorner': self.world_map.get_serialised_south_west_corner(),
            'northEastCorner': self.world_map.get_serialised_north_east_corner(),
            'players': self.avatar_manager.serialise_players(),
            'pickups': serialize_pickups(self.world_map),
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
