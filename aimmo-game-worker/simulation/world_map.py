from .avatar_state import create_avatar_state
from .location import Location
from typing import Dict, List


class Cell(object):

    """
    Any position on the world grid.
    """

    def __init__(self, location, avatar=None, **kwargs):
        self.location = Location(**location)
        self.avatar = None
        self.interactable = None
        self.obstacle = None
        if avatar:
            self.avatar = create_avatar_state(avatar)
        for (key, value) in kwargs.items():
            if not key == "habitable":
                setattr(self, key, value)

    @property
    def habitable(self):
        return not (self.avatar or self.obstacle)

    def has_artefact(self):
        return self.interactable is not None and self.interactable["type"] == "artefact"

    def __repr__(self):
        return "Cell({} a={} i={})".format(
            self.location, self.avatar, self.interactable
        )

    def __eq__(self, other):
        return self.location == other.location

    def __ne__(self, other):
        return not self == other


class WorldMapCreator:
    def generate_world_map_from_cells_data(cells: List[Cell]) -> "WorldMap":
        world_map_cells: Dict[Location, Cell] = {}
        for cell_data in cells:
            cell = Cell(**cell_data)
            world_map_cells[cell.location] = cell
        return WorldMap(world_map_cells)

    def generate_world_map_from_game_state(game_state) -> "WorldMap":
        cells: Dict[Location, Cell] = {}
        for x in range(
            game_state["southWestCorner"]["x"], game_state["northEastCorner"]["x"] + 1
        ):
            for y in range(
                game_state["southWestCorner"]["y"],
                game_state["northEastCorner"]["y"] + 1,
            ):
                cell = Cell({"x": x, "y": y})
                cells[Location(x, y)] = cell

        for interactable in game_state["interactables"]:
            location = Location(
                interactable["location"]["x"], interactable["location"]["y"]
            )
            cells[location].interactable = interactable

        for obstacle in game_state["obstacles"]:
            location = Location(obstacle["location"]["x"], obstacle["location"]["y"])
            cells[location].obstacle = obstacle

        for player in game_state["players"]:
            location = Location(player["location"]["x"], player["location"]["y"])
            cells[location].player = create_avatar_state(player)

        return WorldMap(cells)


class WorldMap(object):

    """
    The non-player world state.
    """

    def __init__(self, cells: Dict[Location, Cell]):
        self.cells = cells

    def all_cells(self):
        return self.cells.values()

    def interactable_cells(self):
        return [cell for cell in self.all_cells() if cell.interactable]

    def pickup_cells(self):
        pickup_types = ("damage_boost", "invulnerability", "health", "artefact")
        return [
            cell
            for cell in self.interactable_cells()
            if cell.interactable["type"] in pickup_types
        ]

    def score_cells(self):
        return [
            cell
            for cell in self.interactable_cells()
            if "score" == cell.interactable["type"]
        ]

    def partially_fogged_cells(self):
        return [cell for cell in self.all_cells() if cell.partially_fogged]

    def is_visible(self, location):
        return location in self.cells

    def get_cell(self, location):
        cell = self.cells[location]
        assert (
            cell.location == location
        ), "location lookup mismatch: arg={}, found={}".format(location, cell.location)
        return cell

    def can_move_to(self, target_location):
        try:
            cell = self.get_cell(target_location)
        except KeyError:
            return False
        return getattr(cell, "habitable", False) and not getattr(cell, "avatar", False)

    def __repr__(self):
        return repr(self.cells)
