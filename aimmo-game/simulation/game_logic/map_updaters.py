import math
import random
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from logging import getLogger

from simulation.cell import Cell
from simulation.interactables.pickups import Artefact
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

    def update(self, world_map, context):
        target_num_pickups = int(
            math.ceil(
                context.num_avatars
                * world_map.settings["TARGET_NUM_PICKUPS_PER_AVATAR"]
            )
        )
        max_num_pickups_to_add = target_num_pickups - len(
            list(world_map.pickup_cells())
        )
        locations = world_map._spawn_location_finder.get_random_spawn_locations(
            max_num_pickups_to_add
        )
        for cell in locations:
            cell.interactable = Artefact(cell)
            LOGGER.info("Adding new pickup at %s of type %s", cell, cell.interactable)


class MapExpander(_MapUpdater):
    def update(self, world_map, context):
        start_size = world_map.num_cells
        target_num_cells = int(
            math.ceil(
                context.num_avatars * world_map.settings["TARGET_NUM_CELLS_PER_AVATAR"]
            )
        )
        num_cells_to_add = target_num_cells - world_map.num_cells
        if num_cells_to_add > 0:
            self._add_outer_layer(world_map)
            assert world_map.num_cells > start_size

    def _add_outer_layer(self, world_map):
        self._add_vertical_layer(world_map, world_map.min_x() - 1)
        self._add_vertical_layer(world_map, world_map.max_x() + 1)
        self._add_horizontal_layer(world_map, world_map.min_y() - 1)
        self._add_horizontal_layer(world_map, world_map.max_y() + 1)

    def _add_vertical_layer(self, world_map, x):
        for y in range(world_map.min_y(), world_map.max_y() + 1):
            world_map.grid[Location(x, y)] = Cell(Location(x, y))

    def _add_horizontal_layer(self, world_map, y):
        for x in range(world_map.min_x(), world_map.max_x() + 1):
            world_map.grid[Location(x, y)] = Cell(Location(x, y))
