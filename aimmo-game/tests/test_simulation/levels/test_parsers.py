from __future__ import absolute_import

from simulation.levels.parsers import Parser
from simulation.levels.transforms import CellTransform

import os
import unittest

class MockTransform():
    def mock(self):
        return "mock"

class MockParser(Parser):
    def __init__(self):
        super(MockParser, self).__init__()
        self._SCRIPT_LOCATION = os.path.abspath(os.path.dirname(__file__))
        self._MAPS_FOLDER = os.path.join(self._SCRIPT_LOCATION, "maps")
        self._MODELS_FOLDER = os.path.join(self._SCRIPT_LOCATION, "models")

    def register_transforms(self, x, y):
        self.register_transform(CellTransform(x, y))
        self.register_transform(MockTransform())

SIMPLE_MODEL = [
  {
    "code": "0",
    "test" : "zero"
  },
  {
    "code": "1",
    "test" : "one"
  }
]

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = MockParser()

    def __with_simple_model(self):
        self.parser.models = []
        self.parser.register_models(["model_simple.json"])

    def __with_big_model(self):
        self.parser.models = []
        self.parser.register_models(["model_simple.json", "model_big.json"])

    def test_parse_simple_map(self):
        self.parser.parse_map("map_simple.txt")
        self.assertItemsEqual(self.parser.map, [
            ['1','2','3','0','0'],
            ['0','0','1','0','2']])

    def test_parse_big_map(self):
        self.parser.parse_map("map_big.txt")
        self.assertEqual(len(self.parser.map), 7)
        self.assertEqual(len(self.parser.map[0]), 11)

    def test_register_models(self):
        self.parser.register_models(["model_simple.json"])
        self.assertEqual(len(self.parser.models), 1)
        self.assertItemsEqual(self.parser.models[0], SIMPLE_MODEL)

    def feed_string(self):
        self.register_transforms(5, 5)
        self.assertEqual(self.parser.feed_string("class:MockTransform.mock"), "mock")
        self.assertEqual(self.parser.feed_string("class:CellTransform.get_x"), 5)
        self.assertEqual(self.parser.feed_string("class:CellTransform.get_y"), 6)
        self.assertEqual(self.parser.feed_string("abc"), "abc")
        self.assertEqual(self.parser.feed_string("CellTransform.get_y"), "CellTransform.get_y")

    def feed_simple_json(self):
        self.__with_simple_model()
        self.register_transforms(0, 0)
        self.assertEqual(self.parser.feed_json("0"), {
          "code": "0",
          "test" : "zero"
        })
        self.assertEqual(self.parser.feed_json("1"), {
          "code": "1",
          "test" : "one"
        })

    def feed_complex_json(self):
        pass
