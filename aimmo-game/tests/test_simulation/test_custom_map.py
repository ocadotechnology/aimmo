from __future__ import absolute_import

import random
import unittest

from simulation.location import Location

from simulation.pickups import HealthPickup
from simulation.pickups import DamagePickup
from simulation.pickups import InvulnerabilityPickup

from simulation.levels.levels import LEVELS
from simulation.custom_map import generate_level_class

from simulation.custom_map import JsonLevelGenerator
from simulation.levels.levels import RawLevelGenerator
from .levels.test_parsers import MockParser

def get_mock_level(map, parsers):
    class MockLevel(JsonLevelGenerator):
        def get_map(self):
            self._register_json(
                RawLevelGenerator()
                    .by_parser(MockParser())
                    .by_map(map)
                    .by_models(parsers)
                    .generate_json())
            self._register_decoders()
            self._json_decode_map()

            return self.world_map
    return MockLevel({})

class TestJsonLevelGenerator(unittest.TestCase):
    def test_json_simple_map(self):
        mock_level = get_mock_level("map_simple.txt", ["real_model.json"])
        mock_map = mock_level.get_map()

        self.assertEquals(mock_map.num_cols, 2)
        self.assertEquals(mock_map.num_rows, 5)

        # 1 2 3 0 0
        # 0 0 1 0 2

        self.assertFalse(mock_map.get_cell(Location(0, 0)).habitable)
        self.assertTrue(mock_map.get_cell(Location(0, 1)).generates_score)
        self.assertTrue(isinstance(mock_map.get_cell(Location(0, 2)).pickup, HealthPickup))
        self.assertTrue(mock_map.get_cell(Location(1, 4)).generates_score)
        self.assertFalse(mock_map.get_cell(Location(1, 2)).habitable)

    def test_json_big_map(self):
        mock_level = get_mock_level("map_big.txt", ["real_model.json"])
        mock_map = mock_level.get_map()

        self.assertEquals(mock_map.num_cols, 7)
        self.assertEquals(mock_map.num_rows, 11)

        # 0 0 0 2 0 0 0 0 0 0 0
        # 0 0 2 2 0 0 0 0 0 0 0
        # 0 0 2 2 0 1 1 1 1 0 0
        # 0 0 0 2 0 0 0 0 1 0 0
        # 0 0 0 0 0 0 0 0 1 0 0
        # 0 0 0 0 0 0 0 0 0 0 0
        # 0 0 0 0 0 0 0 0 0 0 0

        score_locations = [(0,3), (1,2), (1,3), (2,2), (2,3), (3,3)]
        obstacle_locations = [(2,5), (2,6), (2,7), (2,8), (3,8), (4,8)]

        for x, y in score_locations:
            self.assertTrue(mock_map.get_cell(Location(x, y)).generates_score)
        for x, y in obstacle_locations:
            self.assertFalse(mock_map.get_cell(Location(x, y)).habitable)

class TestAutomaticLevelGenerators(unittest.TestCase):
    def test_generate_level_class(self):
        def completed_check(self, y):
            return False

        COMPLETION_CHECKS = {
            "level50" : completed_check
        }
        LEVELS = {
            "level50" : {}
        }
        my_class = generate_level_class(50, LEVELS, COMPLETION_CHECKS)

        self.assertEquals(my_class.__name__, "Level50")
        instance = my_class({})

        self.assertTrue(hasattr(instance, 'get_map'))
        self.assertTrue(hasattr(instance, 'check_complete'))
