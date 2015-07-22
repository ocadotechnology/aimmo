import unittest
import numpy as np
from numpy.testing import assert_array_equal
from simulation.location import Location
from simulation.world_map import WorldMap


def print_array(x):
    print '     ' + '   '.join(str(i) for i in xrange(8))
    for row_label, row in zip(xrange(100), x):
        print '%s [%s]' % (row_label, ' '.join('%03s' % i for i in row))
    print


class TestWorldMap(unittest.TestCase):
    def build_8x8(self):
        return np.arange(64).reshape((8, 8))

    def test_get_world_view_centre_near_middle(self):
        world_map = WorldMap(self.build_8x8())
        world_view = world_map.get_world_view_centred_at(
            Location(row=4, col=3), distance_to_edge=2)

        expected_grid = np.array([
            [17, 18, 19, 20, 21],
            [25, 26, 27, 28, 29],
            [33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45],
            [49, 50, 51, 52, 53],
        ])
        assert_array_equal(world_view, expected_grid)

    def test_get_world_view_centre_near_bottom_left_edge(self):
        world_map = WorldMap(self.build_8x8())
        world_view = world_map.get_world_view_centred_at(
            Location(row=6, col=1), distance_to_edge=2)

        expected_grid = np.array([
            [-1, 32, 33, 34, 35],
            [-1, 40, 41, 42, 43],
            [-1, 48, 49, 50, 51],
            [-1, 56, 57, 58, 59],
            [-1, -1, -1, -1, -1],
        ])
        assert_array_equal(world_view, expected_grid)

    def test_get_world_view_centre_near_top_right_edge(self):
        world_map = WorldMap(self.build_8x8())
        world_view = world_map.get_world_view_centred_at(
            Location(row=1, col=6), distance_to_edge=2)

        expected_grid = np.array([
            [-1, -1, -1, -1, -1],
            [ 4,  5,  6,  7, -1],
            [12, 13, 14, 15, -1],
            [20, 21, 22, 23, -1],
            [28, 29, 30, 31, -1],
        ])
        assert_array_equal(world_view, expected_grid)

    def test_get_world_view_centre_pad_entire(self):
        world_map = WorldMap(self.build_8x8())
        world_view = world_map.get_world_view_centred_at(
            Location(row=4, col=4), distance_to_edge=5)

        expected_grid = np.array([
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1,  0,  1,  2,  3,  4,  5,  6,  7, -1, -1],
            [-1,  8,  9, 10, 11, 12, 13, 14, 15, -1, -1],
            [-1, 16, 17, 18, 19, 20, 21, 22, 23, -1, -1],
            [-1, 24, 25, 26, 27, 28, 29, 30, 31, -1, -1],
            [-1, 32, 33, 34, 35, 36, 37, 38, 39, -1, -1],
            [-1, 40, 41, 42, 43, 44, 45, 46, 47, -1, -1],
            [-1, 48, 49, 50, 51, 52, 53, 54, 55, -1, -1],
            [-1, 56, 57, 58, 59, 60, 61, 62, 63, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ])
        assert_array_equal(world_view, expected_grid)

    def test_get_world_view_centre_pad_entire(self):
        world_map = WorldMap(self.build_8x8())
        world_view = world_map.get_world_view_centred_at(
            Location(row=7, col=3), distance_to_edge=0)

        expected_grid = np.array([[59]])
        assert_array_equal(world_view, expected_grid)
