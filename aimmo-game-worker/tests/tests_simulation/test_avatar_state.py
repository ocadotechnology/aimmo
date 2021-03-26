from __future__ import absolute_import

from unittest import TestCase

from simulation.location import Location
from simulation.avatar_state import create_avatar_state


class TestAvatarState(TestCase):
    AVATAR = {"location": {"x": 0, "y": 0}, "backpack": [{"type": "key"}]}

    def test_create_avatar_state(self):
        avatar_state = create_avatar_state(self.AVATAR)
        avatar_loc = self.AVATAR["location"]

        self.assertEqual(
            avatar_state.location,
            Location(avatar_loc["x"], avatar_loc["y"]),
        )

        self.assertEqual(
            avatar_state.backpack[0].type, self.AVATAR["backpack"][0]["type"]
        )
