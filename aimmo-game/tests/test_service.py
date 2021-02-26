from unittest import TestCase

import service
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_state import GameState
from simulation.interactables.score_location import ScoreLocation
from simulation.location import Location
from simulation.world_map import WorldMap
from .test_simulation.dummy_avatar import MoveEastDummy
from .test_simulation.maps import MockCell, MockPickup
from .test_simulation.mock_game_state import MockGameState
import pytest


@pytest.fixture(scope="module")
def avatar_manager():
    class DummyAvatarManager(AvatarManager):
        avatars = [MoveEastDummy(1, Location(0, -1))]

    return DummyAvatarManager()


@pytest.fixture(scope="module")
def world_state_json(avatar_manager):
    CELLS = [
        [
            {
                "interactable": MockPickup("b"),
                "avatar": avatar_manager.avatars[0],
            },
            {},
            {},
        ],
        [{}, {"habitable": False}, {"interactable": MockPickup("a")}],
    ]

    grid = {
        Location(x, y - 1): MockCell(Location(x, y - 1), **CELLS[x][y])
        for y in range(3)
        for x in range(2)
    }
    grid[Location(0, 1)].interactable = ScoreLocation(grid[Location(0, 1)])
    test_game_state = GameState(WorldMap(grid, {}), avatar_manager)
    return test_game_state.serialize()


def test_correct_json_player_dictionary(world_state_json):
    """
    Ensures the "players" element of the get_game_state() JSON returns the correct information for the dummy
    avatar provided into the world.

    NOTE: Orientation (and others) may be hard coded. This test WILL and SHOULD fail if the functionality is added.
    """
    player_list = world_state_json["players"]
    assert len(player_list) == 1
    details = player_list[0]
    assert details["id"] == 1
    assert details["location"]["x"] == 0
    assert details["location"]["y"] == -1
    assert details["orientation"] == "north"


def test_correct_json_score_locations(world_state_json):
    """
    Ensures the correct score location in the "score_locations" element; is returned by the JSON.
    """
    interactable_list = world_state_json["interactables"]
    for interactable in interactable_list:
        if "ScoreLocation" in interactable:
            assert interactable["location"]["x"] == 0
            assert interactable["location"]["y"] == 1


def test_correct_json_north_east_corner(world_state_json):
    """
    Top right corner of the map must be correct to determine the map size.
    """
    north_east_corner = world_state_json["northEastCorner"]
    assert north_east_corner["x"] == 1
    assert north_east_corner["y"] == 1


def test_correct_json_south_west_corner(world_state_json):
    """
    Bottom left corner of the map must be correct to determine the map size.
    """
    south_west_corner = world_state_json["southWestCorner"]
    assert south_west_corner["x"] == 0
    assert south_west_corner["y"] == -1


def test_correct_json_era(world_state_json):
    """
    Ensure that the era (for the assets in the frontend) is correct.

    NOTE: This is hard coded right now to "future". This test should fail when this functionality is added.
    """
    era = world_state_json["era"]
    assert era == "future"


def test_correct_json_world_interactables_returned_is_correct_amount(world_state_json):
    """
    The JSON returns the correct amount of pickups.
    """
    interactable_list = world_state_json["interactables"]
    assert len(interactable_list) == 3


def test_correct_json_world_obstacles(world_state_json):
    """
    JSON generated must return correct location, width, height, type and orientation about obstacles.

    NOTE: Obstacles are highly hard coded right now. Only location changes. If any functionality is added, this test
            WILL and SHOULD fail.
    """
    obstacle_list = world_state_json["obstacles"]
    assert len(obstacle_list) == 1
    assert obstacle_list[0]["location"]["x"] == 1
    assert obstacle_list[0]["location"]["y"] == 0
    assert obstacle_list[0]["texture"] == 1
