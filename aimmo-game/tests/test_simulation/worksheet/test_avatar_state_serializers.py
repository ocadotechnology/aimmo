from simulation.avatar.avatar_wrapper import AvatarWrapper
from unittest.mock import MagicMock
from simulation.location import Location
from simulation.worksheet.worksheet import worksheets


def test_worksheet1_avatar_state():
    worksheet1 = worksheets[1]
    avatar_wrapper = AvatarWrapper(1, Location(0, 0), MagicMock())
    serialized_avatar_state = worksheet1.avatar_state_serializer(avatar_wrapper)
    assert serialized_avatar_state == {
        "id": 1,
        "orientation": "north",
        "location": {"x": 0, "y": 0},
    }


def test_worksheet2_avatar_state():
    worksheet2 = worksheets[2]
    avatar_wrapper = AvatarWrapper(23, Location(14, -2), MagicMock())
    serialized_avatar_state = worksheet2.avatar_state_serializer(avatar_wrapper)
    assert serialized_avatar_state == {
        "id": 23,
        "location": {"x": 14, "y": -2},
        "orientation": "north",
        "backpack": [],
    }


def test_worksheet3_avatar_state():
    worksheet3 = worksheets[3]
    avatar_wrapper = AvatarWrapper(12, Location(-5, 7), MagicMock())
    serialized_avatar_state = worksheet3.avatar_state_serializer(avatar_wrapper)
    assert serialized_avatar_state == {
        "id": 12,
        "location": {"x": -5, "y": 7},
        "orientation": "north",
        "backpack": [],
    }


def test_worksheet4_avatar_state():
    worksheet4 = worksheets[4]
    avatar_wrapper = AvatarWrapper(32, Location(7, -2), MagicMock())
    serialized_avatar_state = worksheet4.avatar_state_serializer(avatar_wrapper)
    assert serialized_avatar_state == {
        "id": 32,
        "location": {"x": 7, "y": -2},
        "orientation": "north",
        "backpack": [],
    }
