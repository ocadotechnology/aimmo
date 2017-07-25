from __future__ import absolute_import

import random
import unittest

from simulation.location import Location
from simulation.pickups import HealthPickup
from simulation.pickups import DamagePickup
from simulation.pickups import InvulnerabilityPickup

from simulation.world_map import WorldMap
from simulation.custom_map import ScoreCellDecoder
from simulation.custom_map import ObstacleDecoder
from simulation.custom_map import PickupDecoder

from simulation.custom_map import JsonLevelGenerator
from simulation.levels.levels import RawLevelGenerator
from .levels.test_parsers import MockParser

class TestDecoders(unittest.TestCase):
    def setUp(self):
        self.map = WorldMap.generate_empty_map(2, 2, {})

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

    def test_score_cell_decoder(self):
        ScoreCellDecoder("0").decode({
            "x" : "0",
            "y" : "0"
        }, self.map)

        self.assertTrue(self.map.get_cell(Location(0, 0)).generates_score)
        self.assertFalse(self.map.get_cell(Location(0, 1)).generates_score)
        self.assertFalse(self.map.get_cell(Location(1, 0)).generates_score)
        self.assertFalse(self.map.get_cell(Location(1, 1)).generates_score)

        ScoreCellDecoder("0").decode({
            "x" : "1",
            "y" : "1"
        }, self.map)

        self.assertTrue(self.map.get_cell(Location(0, 0)).generates_score)
        self.assertFalse(self.map.get_cell(Location(0, 1)).generates_score)
        self.assertFalse(self.map.get_cell(Location(1, 0)).generates_score)
        self.assertTrue(self.map.get_cell(Location(1, 1)).generates_score)

    def test_pickup_decoder(self):
        PickupDecoder("0").decode({
            "x" : "0",
            "y" : "1",
            "type" : "health",
            "health_restored" : "5"
        }, self.map)
        PickupDecoder("0").decode({
            "x" : "1",
            "y" : "0",
            "type" : "damage"
        }, self.map)
        PickupDecoder("0").decode({
            "x" : "1",
            "y" : "1",
            "type" : "invulnerability"
        }, self.map)

        self.assertTrue(self.map.get_cell(Location(0, 0)).pickup is None)
        self.assertTrue(isinstance(self.map.get_cell(Location(0, 1)).pickup, HealthPickup))
        self.assertTrue(isinstance(self.map.get_cell(Location(1, 0)).pickup, DamagePickup))
        self.assertTrue(isinstance(self.map.get_cell(Location(1, 1)).pickup, InvulnerabilityPickup))

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

        # for cell in mock_map.all_cells():
        #     print("CELL: (" + str(cell.location.x) + " " + str(cell.location.y) + ")")
