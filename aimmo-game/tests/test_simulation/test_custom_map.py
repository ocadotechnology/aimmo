from __future__ import absolute_import

import random
import unittest

from simulation.location import Location

from simulation.custom_map import EmptyMapGenerator
from simulation.custom_map import ScoreCellDecoder
from simulation.custom_map import ObstacleDecoder
from simulation.custom_map import PickupDecoder

class TestGenerators(unittest.TestCase):
    def setUp(self):
        self.map = EmptyMapGenerator(2, 2, {}).get_map()

    def test_obstacle_decoder(self):
        ObstacleDecoder("0").decode({
            "x" : "0",
            "y" : "0"
        }, self.map)

        self.assertFalse(self.map.get_cell(Location(0, 0)).habitable)
        self.assertTrue(self.map.get_cell(Location(0, 1)).habitable)
        self.assertTrue(self.map.get_cell(Location(1, 0)).habitable)
        self.assertTrue(self.map.get_cell(Location(1, 1)).habitable)

        ObstacleDecoder("0").decode({
            "x" : "1",
            "y" : "1"
        }, self.map)

        self.assertFalse(self.map.get_cell(Location(0, 0)).habitable)
        self.assertTrue(self.map.get_cell(Location(0, 1)).habitable)
        self.assertTrue(self.map.get_cell(Location(1, 0)).habitable)
        self.assertFalse(self.map.get_cell(Location(1, 1)).habitable)
