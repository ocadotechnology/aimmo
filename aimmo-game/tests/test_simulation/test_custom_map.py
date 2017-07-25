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

class TestGenerators(unittest.TestCase):
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
