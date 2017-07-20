from __future__ import absolute_import

from simulation.levels.parsers import Parser

import os
import unittest

class MockParser(Parser):
    def __init__(self):
        super(MockParser, self).__init__()
        self._SCRIPT_LOCATION = os.path.abspath(os.path.dirname(__file__))
        self._MAPS_FOLDER = os.path.join(self._SCRIPT_LOCATION, "maps")
        self._MODELS_FOLDER = os.path.join(self._SCRIPT_LOCATION, "models")

    def register_transforms(self, x, y):
        pass

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = MockParser()

    def test_parse_simple_map(self):
        self.parser.parse_map("map_simple.txt")
        self.assertItemsEqual(self.parser.map, [
            ['1','2','3','0','0'],
            ['0','0','1','0','2']])

    def test_parse_big_map(self):
        self.parser.parse_map("map_big.txt")
        self.assertEqual(len(self.parser.map), 7)
        self.assertEqual(len(self.parser.map[0]), 11)
