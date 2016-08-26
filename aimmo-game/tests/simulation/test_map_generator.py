from __future__ import absolute_import
import unittest
from simulation.map_generator import get_random_edge_index, generate_map


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
        m = generate_map(4, 3, 1.0)
        grid = list(m.all_cells)
        self.assertEqual(len(set(grid)), len(grid), "Repeats in list")
        for c in grid:
            self.assertLess(c.location.x, 3)
            self.assertLess(c.location.y, 4)
            self.assertGreaterEqual(c.location.x, 0)
            self.assertGreaterEqual(c.location.y, 0)

    def test_obstacle_ratio(self):
        m = generate_map(10, 10, 0.0)
        obstacle_cells = [cell for cell in m.all_cells if not cell.is_habitable]
        self.assertEqual(len(obstacle_cells), 0)

    def test_map_contains_some_non_habitable_cell(self):
        m = generate_map(4, 4, 1.0)
        obstacle_cells = [cell for cell in m.all_cells if not cell.is_habitable]
        self.assertGreaterEqual(len(obstacle_cells), 1)

    def test_map_contains_some_habitable_cell_on_border(self):
        m = generate_map(4, 4, 1.0)

        edge_coordinates = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (3, 1),
            (0, 2), (3, 2),
            (0, 3), (1, 3), (2, 3), (3, 3)
        ]
        edge_cells = (m._grid[x][y] for (x, y) in edge_coordinates)
        habitable_edge_cells = [cell for cell in edge_cells if cell.is_habitable]

        self.assertGreaterEqual(len(habitable_edge_cells), 1)
