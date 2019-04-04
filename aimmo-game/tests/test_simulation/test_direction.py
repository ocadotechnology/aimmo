from __future__ import absolute_import

from unittest import TestCase

from simulation.direction import Direction
from simulation.location import Location


class TestDirection(TestCase):
    def test_good_data(self):
        d = Direction(0, 1)
        self.assertEqual(d.x, 0)
        self.assertEqual(d.y, 1)

    def test_high_x(self):
        with self.assertRaises(ValueError):
            Direction(1.5, 0)

    def test_low_x(self):
        with self.assertRaises(ValueError):
            Direction(-1.5, 0)

    def test_high_y(self):
        with self.assertRaises(ValueError):
            Direction(0, 1.5)

    def test_low_y(self):
        with self.assertRaises(ValueError):
            Direction(0, -1.5)

    def test_too_far(self):
        with self.assertRaises(ValueError):
            Direction(1, 1)

    def test_repr(self):
        txt = repr(Direction(1, 0))
        self.assertRegex(txt, "x *= *1")
        self.assertRegex(txt, "y *= *0")

    def test_incorrect_equality(self):
        d1 = Direction(0, 1)
        l1 = Location(0, 1)
        self.assertFalse(d1 == l1)
