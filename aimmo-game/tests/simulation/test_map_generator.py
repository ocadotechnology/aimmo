from __future__ import absolute_import
import unittest
from simulation.map_generator import get_random_edge_index, generate_map
from simulation.location import Location


class ConstantRng(object):

    def __init__(self, value):
        self.value = value

    def randint(self, minimum, maximum):
        if not minimum <= self.value <= maximum:
            raise ValueError('Beyond range')
        return self.value


class TestMapGenerator(unittest.TestCase):

    def test_get_random_edge_index(self):
        height, width = 3, 4
        # First row
        self.assertEqual(
            (1, 0), get_random_edge_index(height, width, rng=ConstantRng(0)))
        self.assertEqual(
            (2, 0), get_random_edge_index(height, width, rng=ConstantRng(1)))

        # Last row
        self.assertEqual(
            (1, 2), get_random_edge_index(height, width, rng=ConstantRng(2)))
        self.assertEqual(
            (2, 2), get_random_edge_index(height, width, rng=ConstantRng(3)))

        # First column
        self.assertEqual(
            (0, 1), get_random_edge_index(height, width, rng=ConstantRng(4)))

        # Last column
        self.assertEqual(
            (3, 1), get_random_edge_index(height, width, rng=ConstantRng(5)))

        # Verify no out of bounds
        with self.assertRaisesRegexp(ValueError, 'Beyond range'):
            get_random_edge_index(height, width, rng=ConstantRng(-1))

        with self.assertRaisesRegexp(ValueError, 'Beyond range'):
            get_random_edge_index(height, width, rng=ConstantRng(6))

    def test_map_dimensions(self):
        settings = {
            'START_WIDTH': 3,
            'START_HEIGHT': 4,
            'OBSTACLE_RATIO': 1.0
        }
        m = generate_map(settings)
        grid = list(m.all_cells())
        self.assertEqual(len(set(grid)), len(grid), "Repeats in list")
        for c in grid:
            self.assertLess(c.location.x, 3)
            self.assertLess(c.location.y, 4)
            self.assertGreaterEqual(c.location.x, 0)
            self.assertGreaterEqual(c.location.y, 0)

    def test_obstable_ratio(self):
        settings = {
            'START_WIDTH': 3,
            'START_HEIGHT': 4,
            'OBSTACLE_RATIO': 0
        }
        m = generate_map(settings)
        obstacle_cells = [cell for row in m.grid for cell in row if not cell.habitable]
        self.assertEqual(len(obstacle_cells), 0)

    def test_map_contains_some_non_habitable_cell(self):
        settings = {
            'START_WIDTH': 4,
            'START_HEIGHT': 4,
            'OBSTACLE_RATIO': 1.0
        }
        m = generate_map(settings)
        obstacle_cells = [cell for row in m.grid for cell in row if not cell.habitable]
        self.assertGreaterEqual(len(obstacle_cells), 1)

    def test_map_contains_some_habitable_cell_on_border(self):
        settings = {
            'START_WIDTH': 4,
            'START_HEIGHT': 4,
            'OBSTACLE_RATIO': 1.0
        }
        m = generate_map(settings)
        edge_coordinates = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (3, 1),
            (0, 2), (3, 2),
            (0, 3), (1, 3), (2, 3), (3, 3)
        ]
        edge_cells = (m.get_cell(Location(x, y)) for (x, y) in edge_coordinates)
        habitable_edge_cells = [cell for cell in edge_cells if cell.habitable]

        self.assertGreaterEqual(len(habitable_edge_cells), 1)
