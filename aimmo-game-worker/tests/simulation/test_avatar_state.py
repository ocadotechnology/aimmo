from __future__ import absolute_import

from unittest import TestCase
from simulation.avatar_state import AvatarState


class TestAvatarState(TestCase):

    def test_constructor_avatar_state(self):
        dummy_avatar_state = AvatarState({'x': 0, 'y': 1}, 10, 5, 2)
        self.assertEquals(dummy_avatar_state.location.x, 0)
        self.assertEquals(dummy_avatar_state.location.y, 1)

        self.assertEquals(dummy_avatar_state.health, 10)
        self.assertEquals(dummy_avatar_state.score, 5)
        self.assertEquals(dummy_avatar_state.events, 2)