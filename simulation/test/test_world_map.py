import unittest
from simulation import world_map
from simulation.location import Location


class TestWorldMap(unittest.TestCase):
    def test_bisects_map(self):
        m = world_map.generate_map(3, 1, 0)
        middle_cell = m.get_cell(Location(0, 1))
        self.assertFalse(world_map.bisects_map(middle_cell, m))
        middle_cell.habitable = False
        self.assertTrue(world_map.bisects_map(middle_cell, m))

