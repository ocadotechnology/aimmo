from threading import RLock

from simulation.interactables import serialize_interactables
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.world_map import WorldMap


class GameState:
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """

    def __init__(
        self, world_map, avatar_manager, completion_check_callback=lambda: None
    ):
        self.world_map: "WorldMap" = world_map
        self.avatar_manager = avatar_manager
        self.main_avatar_id = None
        self.turn_count = 0
        self._lock = RLock()

    def get_main_avatar(self):
        with self._lock:
            return self.avatar_manager.avatars_by_id[self.main_avatar_id]

    def serialize(self):
        return {
            "era": "future",
            "southWestCorner": self.world_map.get_serialized_south_west_corner(),
            "northEastCorner": self.world_map.get_serialized_north_east_corner(),
            "players": self.avatar_manager.serialize_players(),
            "interactables": serialize_interactables(self.world_map),
            "obstacles": self.world_map.serialize_obstacles(),
            "turnCount": self.turn_count,
        }
