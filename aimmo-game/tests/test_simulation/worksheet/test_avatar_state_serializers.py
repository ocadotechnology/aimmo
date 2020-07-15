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

