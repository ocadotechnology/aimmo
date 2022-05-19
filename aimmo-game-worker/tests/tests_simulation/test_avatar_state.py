import pytest

from simulation.location import Location
from simulation.avatar_state import create_avatar_state


@pytest.fixture
def avatar_state_json():
    return {"location": {"x": 0, "y": 0}, "backpack": [{"type": "key"}]}


@pytest.fixture
def avatar_state_json_no_backpack():
    return {"location": {"x": 1, "y": 1}}


def test_create_avatar_state(avatar_state_json):
    avatar_state = create_avatar_state(avatar_state_json)
    avatar_loc = avatar_state_json["location"]

    assert avatar_state.location == Location(avatar_loc["x"], avatar_loc["y"])
    assert avatar_state.backpack[0].type == avatar_state_json["backpack"][0]["type"]


def test_create_avatar_state_no_backpack(avatar_state_json_no_backpack):
    avatar_state = create_avatar_state(avatar_state_json_no_backpack)
    avatar_loc = avatar_state_json_no_backpack["location"]

    assert avatar_state.location == Location(avatar_loc["x"], avatar_loc["y"])
    assert not hasattr(avatar_state, "backpack")
