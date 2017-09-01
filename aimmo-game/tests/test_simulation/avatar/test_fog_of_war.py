from __future__ import absolute_import

from unittest import TestCase

from simulation.avatar.fog_of_war import should_partially_fog


class TestFogOfWar(TestCase):
    def test_should_partially_fog(self):
        self.assertFalse(should_partially_fog(no_fog_distance=20, partial_fog_distance=2, x_dist=1, y_dist=10))
        self.assertTrue(should_partially_fog(no_fog_distance=1, partial_fog_distance=2, x_dist=20, y_dist=10))




