import unittest
from simulation import world_map
from simulation.location import Location
import simulation.map_generator


class TestWorldMap(unittest.TestCase):
    def test_bisects_map(self):
        m = simulation.map_generator.generate_map(3, 1, 0)
        middle_cell = m.get_cell(Location(0, 1))
        self.assertFalse(simulation.map_generator.bisects_map(middle_cell, m))
        middle_cell.habitable = False
        self.assertTrue(simulation.map_generator.bisects_map(middle_cell, m))

