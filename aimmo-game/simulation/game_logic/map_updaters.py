import math
import random
from abc import ABCMeta, abstractmethod
from collections import Counter, namedtuple
from logging import getLogger
from typing import List, Type

from simulation.cell import Cell
from simulation.interactables.interactable import _Interactable
from simulation.interactables.score_location import ScoreLocation
from simulation.location import Location

LOGGER = getLogger(__name__)

MapContext = namedtuple("MapContext", "num_avatars")


class _MapUpdater:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, world_map, context):
        raise NotImplementedError


class ScoreLocationUpdater(_MapUpdater):
    def update(self, world_map, context):
        for cell in world_map.score_cells():
            if random.random() < world_map.settings["SCORE_DESPAWN_CHANCE"]:
                cell.interactable.delete()

        new_num_score_locations = len(list(world_map.score_cells()))
        target_num_score_locations = int(
            math.ceil(
                context.num_avatars
                * world_map.settings["TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR"]
            )
        )
        num_score_locations_to_add = (
            target_num_score_locations - new_num_score_locations
        )
        locations = world_map._spawn_location_finder.get_random_spawn_locations(
            num_score_locations_to_add
        )
        for cell in locations:
            cell.interactable = ScoreLocation(cell)


class PickupUpdater(_MapUpdater):
    """
    Generates artefacts based on the TARGET_NUM_PICKUPS_PER_AVATAR setting.
    """

    def __init__(self, pickup_types: List[Type[_Interactable]]) -> None:
        super().__init__()
        self.pickup_types = pickup_types

    def update(self, world_map, context):
        target_total_num_pickups = (
            context.num_avatars * world_map.settings["TARGET_NUM_PICKUPS_PER_AVATAR"]
        )
        target_num_pickups_per_type = int(
            math.ceil(target_total_num_pickups / len(self.pickup_types))
        )
        current_num_pickups = Counter(
            type(cell.interactable) for cell in world_map.pickup_cells()
        )
        for pickup_type in self.pickup_types:
            max_num_pickups_to_add = (
                target_num_pickups_per_type - current_num_pickups[pickup_type]
            )
            locations = world_map._spawn_location_finder.get_random_spawn_locations(
                max_num_pickups_to_add
            )
            for cell in locations:
                cell.interactable = pickup_type(cell)
                LOGGER.info(
                    "Adding new pickup at %s of type %s", cell, cell.interactable
                )
