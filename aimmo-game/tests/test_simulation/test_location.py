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

        loc_2 = Location(0, 0)
        expected = Location(1, 2)
        self.assertEqual(loc_1 - loc_2, expected)

    def test_hash_equal(self):
        loc_1 = Location(3, 3)
        loc_2 = Location(3, 3)
        self.assertEqual(hash(loc_1), hash(loc_2))

    def test_location_raises_exception_with_floats(self):
        self.assertRaises(TypeError, Location, 3.2, 3)
        self.assertRaises(TypeError, Location, 2, 2.2)
        self.assertRaises(TypeError, Location, 2.5, 2.5)
        self.assertRaises(TypeError, Location, 2.0, 1)
