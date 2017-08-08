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

    def register_transforms(self, x, y, width=None, height=None):
        # If we want to keep the same coordinates, we can make the width and
        # height double to keep the same x and y position of coordinates 
        if width is None: width = x * 2 + 1
        if height is None: height = y * 2 + 1

        self.register_transform(CellTransform(x, y, width, height))
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

    def __with_big_map(self):
        self.parser.parse_map("map_big.txt")

    def __with_simple_map(self):
        self.parser.parse_map("map_simple.txt")

    def __with_micro_map(self):
        self.parser.parse_map("map_micro.txt")

    def test_parse_simple_map(self):
        self.__with_simple_map()
        self.assertItemsEqual(self.parser.map, [
            ['1','2','3','0','0'],
            ['0','0','1','0','2']])

    def test_parse_big_map(self):
        self.__with_big_map()
        self.assertEqual(len(self.parser.map), 7)
        self.assertEqual(len(self.parser.map[0]), 11)

    def test_register_models(self):
        self.__with_simple_model()
        self.assertEqual(len(self.parser.models), 1)
        self.assertItemsEqual(self.parser.models[0], SIMPLE_MODEL)

    def test_feed_string(self):
        self.__with_simple_model()
        self.parser.register_transforms(5, 5)
        self.assertEqual(self.parser.feed_string("class:MockTransform.mock"), "mock")
        self.assertEqual(self.parser.feed_string("class:CellTransform.get_x"), '5')
        self.assertEqual(self.parser.feed_string("class:CellTransform.get_y"), '5')
        self.assertEqual(self.parser.feed_string("abc"), "abc")
        self.assertEqual(self.parser.feed_string("CellTransform.get_y"), "CellTransform.get_y")

    def test_feed_simple_json(self):
        self.__with_simple_model()
        self.parser.register_transforms(0, 0)
        self.assertItemsEqual(self.parser.feed_json("0"), {
          "code": "0",
          "test" : "zero"
        })
        self.assertItemsEqual(self.parser.feed_json("1"), {
          "code": "1",
          "test" : "one"
        })

    def test_feed_big_json(self):
        self.__with_big_model()
        self.__with_big_map()
        self.parser.register_transforms(0, 0)
        self.assertItemsEqual(self.parser.feed_json("0"), {
          "code": "0",
          "test" : "zero"
        })
        self.parser.register_transforms(3, 3)
        self.assertItemsEqual(self.parser.feed_json("2"), {
            "code": "2",
            "test" : {
                "big" : "big",
                "cool" : "cool"
                },
            "x" : '3',
            "other" : {
                "y" : '3',
                "test" : "mock"
            }
        })

    def test_map_apply_transforms(self):
        self.__with_micro_map()
        self.__with_big_model()

        self.assertItemsEqual(self.parser.map_apply_transforms(), [{
            "code": "0",
            "test" : "zero"
         }, {
            "code": "1",
            "test" : "one"
         }, {
             "code": "2",
             "test" : {
                 "big" : "big",
                 "cool" : "cool"
                 },
             "x" : '0',
             "other" : {
                 "y" : '2',
                 "test" : "mock"
             }
         }])

    def test_map_apply_transforms_big_map(self):
        self.__with_big_model()
        self.__with_big_map()
        self.assertEqual(len(self.parser.map_apply_transforms()), 77)

        self.__with_simple_model()
        self.__with_big_map()
        self.assertEqual(len(self.parser.map_apply_transforms()), 71)

        self.__with_big_model()
        self.__with_simple_map()
        self.assertEqual(len(self.parser.map_apply_transforms()), 9)
