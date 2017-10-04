from __future__ import absolute_import

from unittest import TestCase

from simulation.geography.location import Location


class TestLocation(TestCase):

    def test_add(self):
        dummy_location = Location(1, 2)
        direction = Location(1, 1)
        expected = Location(2, 3)
        self.assertEqual(dummy_location + direction, expected)

    def test_sub(self):
        dummy_location = Location(3, 2)
        direction = Location(1, 1)
        expected = Location(2, 1)
        self.assertEqual(dummy_location - direction, expected)

    def test_repr(self):
        dummy_location = Location(1, 2)
        self.assertTrue("Location(1, 2)" == str(dummy_location))

    def test_not_equal(self):
        dummy_location_1 = Location(1, 1)
        dummy_location_2 = Location(2, 2)
        self.assertTrue(dummy_location_1 != dummy_location_2)
