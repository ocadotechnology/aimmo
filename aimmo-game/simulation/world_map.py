import math
from logging import getLogger

from simulation.cell import Cell
from simulation.game_logic import SpawnLocationFinder
from simulation.interactables.pickups import ALL_PICKUPS
from simulation.interactables.score_location import ScoreLocation
from simulation.level_settings import DEFAULT_LEVEL_SETTINGS
from simulation.location import Location

LOGGER = getLogger(__name__)


class WorldMap(object):
    """
    The non-player world state.
    """

    def __init__(self, grid, settings):
        """
        :param grid: All types of cells to be inserted into the map.
        :param settings: Constant values provided when generating a level/map.
        """
        self.grid = grid
        self.settings = settings
        self._spawn_location_finder = SpawnLocationFinder(self)

    @classmethod
    def _min_max_from_dimensions(cls, height, width):
        """
        The value provided by the user will be an integer both for the width and height
        components. We calculate the maximum and minimum dimensions in all directions.
        """
        max_x = int(math.floor(width / 2))
        min_x = -(width - max_x - 1)
        max_y = int(math.floor(height / 2))
        min_y = -(height - max_y - 1)
        return min_x, max_x, min_y, max_y

    @classmethod
    def generate_empty_map(cls, height, width, settings):
        new_settings = DEFAULT_LEVEL_SETTINGS.copy()
        new_settings.update(settings)

        (min_x, max_x, min_y, max_y) = WorldMap._min_max_from_dimensions(height, width)
        grid = {}
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                location = Location(x, y)
                grid[location] = Cell(location)
        return cls(grid, new_settings)

    def all_cells(self):
        return self.grid.values()

    def interactable_cells(self):
        return (cell for cell in self.all_cells() if cell.interactable)

    def score_cells(self):
        return (
            cell
            for cell in self.all_cells()
            if isinstance(cell.interactable, ScoreLocation)
        )

    def pickup_cells(self):
        return (
            cell
            for cell in self.all_cells()
            if isinstance(cell.interactable, ALL_PICKUPS)
        )

    def is_on_map(self, location):
        try:
            self.grid[location]
        except KeyError:
            return False
        return True

    def get_cell(self, location) -> Cell:
        try:
            return self.grid[location]
        except KeyError:
            # For backwards-compatibility, this throws ValueError
            raise ValueError("Location %s is not on the map" % location)

    def get_cell_by_coords(self, x, y):
        return self.get_cell(Location(x, y))

    def clear_cell_actions(self, location):
        try:
            cell = self.get_cell(location)
            cell.actions = []
        except ValueError:
            return

    def max_y(self):
        return max(self.grid.keys(), key=lambda c: c.y).y

    def min_y(self):
        return min(self.grid.keys(), key=lambda c: c.y).y

    def max_x(self):
        return max(self.grid.keys(), key=lambda c: c.x).x

    def min_x(self):
        return min(self.grid.keys(), key=lambda c: c.x).x

    @property
    def num_rows(self):
        return self.max_y() - self.min_y() + 1

    @property
    def num_cols(self):
        return self.max_x() - self.min_x() + 1

    @property
    def num_cells(self):
        return self.num_rows * self.num_cols

    def can_move_to(self, target_location):
        if not self.is_on_map(target_location):
            return False
        cell = self.get_cell(target_location)

        return (
            cell.habitable
            and (not cell.is_occupied or cell.avatar.is_moving)
            and len(cell.moves) <= 1
        )

    def attackable_avatar(self, target_location):
        """
        Return a boolean if the avatar is attackable at the given location (or will be
        after next move), else return None.
        """
        try:
            cell = self.get_cell(target_location)
        except ValueError:
            return None

        if cell.avatar:
            return cell.avatar

        if len(cell.moves) == 1:
            return cell.moves[0].avatar

        return None

    def get_no_fog_distance(self):
        return self.settings["NO_FOG_OF_WAR_DISTANCE"]

    def get_partial_fog_distance(self):
        return self.settings["PARTIAL_FOG_OF_WAR_DISTANCE"]

    def get_random_spawn_location(self):
        return self._spawn_location_finder.get_random_spawn_location()

    def __repr__(self):
        return repr(self.grid)

    def __iter__(self):
        return (
            (
                self.get_cell(Location(x, y))
                for y in range(self.min_y(), self.max_y() + 1)
            )
            for x in range(self.min_x(), self.max_x() + 1)
        )

    # Serialisation Utilities
    def get_serialized_south_west_corner(self):
        """
        Used in serialising the map size when sent to the front end. Very lightweight as
        it consists of two integers.

        :return: A dictionary with two values, x and y coordinates for the bottom left
        (south-west) corner of the map.
        """
        return {"x": self.min_x(), "y": self.min_y()}

    def get_serialized_north_east_corner(self):
        """
        Used in serialising the map size when sent to the front end. Very lightweight as
        it consists of two integers.

        :return: A dictionary with two values, x and y coordinates for the top right
        (north-west) corner of the map.
        """
        return {"x": self.max_x(), "y": self.max_y()}

    def serialize_score_location(self):
        """
        Used to serialize the score locations on every update.

        :return: A single list that contains all score locations. Within
        the list there are x and y coordinates.
        """

        def get_coords(cell):
            return {"location": {"x": cell.location.x, "y": cell.location.y}}

        return [
            get_coords(cell)
            for cell in self.all_cells()
            if isinstance(cell.interactable, ScoreLocation)
        ]

    def serialize_obstacles(self):
        """
        Used to serialize the obstacle locations on every update.

        :return: A list that contains all the obstacle information generated by inner method.
        """

        def serialize_obstacle(cell):
            return {
                "location": {"x": cell.location.x, "y": cell.location.y},
                "width": 1,
                "height": 1,
                "type": "wall",
                "orientation": "north",
            }

        return [
            serialize_obstacle(cell) for cell in self.all_cells() if not cell.habitable
        ]


def WorldMapStaticSpawnDecorator(world_map, spawn_location):
    world_map._spawn_location_finder.get_random_spawn_location = lambda: spawn_location
    return world_map
