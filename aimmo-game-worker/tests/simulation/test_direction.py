from __future__ import absolute_import

from unittest import TestCase
from simulation.direction import Direction
from simulation.direction import NORTH, EAST, SOUTH, WEST, ALL_DIRECTIONS


class TestDirection(TestCase):

    def test_constructing_direction_complete(self):
        direction = Direction(10, 20)
        self.assertEqual(direction.x, 10)
        self.assertEqual(direction.y, 20)
        self.assertTrue(type(direction) is Direction)

    def test_incorrect_constructor(self):
        self.failUnlessRaises(Direction)

    def test_direction_repr(self):
        direction1 = Direction(10, 20)
        direction2 = Direction(10, 20)
        self.assertTrue(eval('repr(direction1)' + '==' + 'repr(direction2)'))

        direction2 = Direction(1, 1)
        self.assertFalse(eval('repr(direction1)' + '==' + 'repr(direction2)'))

    def test_direction_serialise(self):
        direction = Direction(103, 20)
        self.assertEqual(direction.serialise()['x'], 103)
        self.assertEqual(direction.serialise()['y'], 20)

    def test_precreated_directions(self):
        self.assertEqual(NORTH.serialise()['x'], 0)
        self.assertEqual(NORTH.serialise()['y'], 1)
        self.assertEqual(EAST.serialise()['x'], 1)
        self.assertEqual(EAST.serialise()['y'], 0)
        self.assertEqual(SOUTH.serialise()['x'], 0)
        self.assertEqual(SOUTH.serialise()['y'], -1)
        self.assertEqual(WEST.serialise()['x'], -1)
        self.assertEqual(WEST.serialise()['y'], 0)

    def test_all_directions(self):
        self.assertTrue(NORTH in ALL_DIRECTIONS)
        self.assertTrue(EAST in ALL_DIRECTIONS)
        self.assertTrue(SOUTH in ALL_DIRECTIONS)
        self.assertTrue(WEST in ALL_DIRECTIONS)

        self.assertTrue(ALL_DIRECTIONS.__len__() == 4)
