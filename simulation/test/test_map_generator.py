import unittest
from simulation.map_generator import get_random_edge_index


class ConstantRng:

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