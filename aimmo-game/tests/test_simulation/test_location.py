from __future__ import absolute_import

from unittest import TestCase

from simulation.location import Location


class TestLocation(TestCase):
    def test_equal(self):
        loc_1 = Location(3, 3)
        loc_2 = Location(3, 3)
        self.assertEqual(loc_1, loc_2)
        self.assertFalse(loc_1 != loc_2)

    def test_x_not_equal(self):
        loc_1 = Location(3, 3)
        loc_2 = Location(4, 3)
        self.assertNotEqual(loc_1, loc_2)
        self.assertFalse(loc_1 == loc_2)

    def test_y_not_equal(self):
        loc_1 = Location(4, 4)
        loc_2 = Location(4, 3)
        self.assertNotEqual(loc_1, loc_2)
        self.assertFalse(loc_1 == loc_2)

    def test_add(self):
        loc_1 = Location(1, 2)
        loc_2 = Location(3, 4)
        expected = Location(4, 6)
        self.assertEqual(loc_1 + loc_2, expected)

    def test_sub(self):
        loc_1 = Location(1, 2)
        loc_2 = Location(3, 4)
        expected = Location(-2, -2)
        self.assertEqual(loc_1 - loc_2, expected)

    def test_hash_equal(self):
        loc_1 = Location(3, 3)
        loc_2 = Location(3, 3)
        self.assertEqual(hash(loc_1), hash(loc_2))

    def test_serialise(self):
        loc = Location(3, 9)
        expected = {'x': 3, 'y': 9}
        self.assertEqual(loc.serialise(), expected)
