from enum import Enum
from threading import RLock

from simulation.interactables import serialize_interactables


class GameState:
    """
    Encapsulates the entire game state, including avatars, their code, and the world.
    """

    def __init__(
        self, world_map, avatar_manager, completion_check_callback=lambda: None
    ):
        self.world_map = world_map
        self.avatar_manager = avatar_manager
        self.main_avatar_id = None
        self.turn_count = 0
        self._lock = RLock()

    def get_main_avatar(self):
        with self._lock:
            return self.avatar_manager.avatars_by_id[self.main_avatar_id]

    def serialize(self):
        return {
            "era": "less_flat",
            "southWestCorner": self.world_map.get_serialized_south_west_corner(),
            "northEastCorner": self.world_map.get_serialized_north_east_corner(),
            "players": self.avatar_manager.serialize_players(),
            "interactables": serialize_interactables(self.world_map),
            "obstacles": self.world_map.serialize_obstacles(),
        }

    def serialize_for_worker(self, avatar_wrapper):
        with self._lock:
            return {
                "avatar_state": avatar_wrapper.serialize(),
                "world_map": {
                    "cells": [cell.serialize() for cell in self.world_map.all_cells()]
                },
            }

    def get_serialized_game_states_for_workers(self):
        with self._lock:
            return {
                player_id: self.serialize_for_worker(avatar_wrapper)
                for player_id, avatar_wrapper in self.avatar_manager.avatars_by_id.items()
            }
