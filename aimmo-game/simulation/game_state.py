from __future__ import annotations

from typing import TYPE_CHECKING

from simulation.interactables import serialize_interactables
from simulation.worksheet.worksheet import get_worksheet_data

if TYPE_CHECKING:
    from simulation.world_map import WorldMap
    from simulation.avatar.avatar_manager import AvatarManager
    from simulation.worksheet.worksheet import WorksheetData


class GameState:
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """

    def __init__(self, world_map, avatar_manager, worksheet: WorksheetData = None):
        if worksheet is None:
            worksheet = get_worksheet_data()

        self.world_map: WorldMap = world_map
        self.avatar_manager: AvatarManager = avatar_manager
        self.turn_count: int = 0
        self.worksheet: WorksheetData = worksheet

    def serialize(self):
        return {
            "era": self.worksheet.era,
            "southWestCorner": self.world_map.get_serialized_south_west_corner(),
            "northEastCorner": self.world_map.get_serialized_north_east_corner(),
            "players": self.avatar_manager.serialize_players(),
            "interactables": serialize_interactables(self.world_map),
            "obstacles": self.world_map.serialize_obstacles(),
            "turnCount": self.turn_count,
        }
