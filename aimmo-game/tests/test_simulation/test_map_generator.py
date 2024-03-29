from __future__ import absolute_import

import random
import unittest

from simulation import map_generator
from simulation.location import Location
from simulation.map_generator import get_random_edge_index
from simulation.simulation_runner import SequentialSimulationRunner
from simulation.world_map import WorldMap

from .dummy_avatar import DummyAvatarManager


class ConstantRng(object):
    def __init__(self, value):
        self.value = value

    def randint(self, minimum, maximum):
        if not minimum <= self.value <= maximum:
            raise ValueError("Beyond range")
        return self.value


class TestHelperFunctions(unittest.TestCase):
    def test_get_random_edge_index(self):
        map = WorldMap.generate_empty_map(3, 4, {})
        assert (0, -1) == get_random_edge_index(map, rng=ConstantRng(0))
        assert (1, -1) == get_random_edge_index(map, rng=ConstantRng(1))
        assert (0, 1) == get_random_edge_index(map, rng=ConstantRng(2))
        assert (1, 1) == get_random_edge_index(map, rng=ConstantRng(3))
        assert (-1, 0) == get_random_edge_index(map, rng=ConstantRng(4))
        assert (2, 0) == get_random_edge_index(map, rng=ConstantRng(5))

        # Verify no out of bounds
        with self.assertRaisesRegex(ValueError, "Beyond range"):
            get_random_edge_index(map, rng=ConstantRng(-1))

        with self.assertRaisesRegex(ValueError, "Beyond range"):
            get_random_edge_index(map, rng=ConstantRng(6))

    def test_get_random_edge_index_can_give_all_possible(self):
        map = WorldMap.generate_empty_map(3, 4, {})
        get_random_edge_index(map, rng=ConstantRng(1))
        expected = frozenset(((0, 1), (1, 1), (-1, 0), (2, 0), (0, -1), (1, -1)))
        actual = frozenset(
            get_random_edge_index(map, rng=ConstantRng(i)) for i in range(6)
        )
        assert expected == actual

    def test_out_of_bounds_random_edge(self):
        map = WorldMap.generate_empty_map(3, 4, {})
        with self.assertRaisesRegex(ValueError, "Beyond range"):
            get_random_edge_index(map, rng=ConstantRng(-1))

        with self.assertRaisesRegex(ValueError, "Beyond range"):
            get_random_edge_index(map, rng=ConstantRng(6))


class _BaseGeneratorTestCase(unittest.TestCase):
    def get_game_state(self, **kwargs):
        random.seed(0)
        settings = {"START_WIDTH": 3, "START_HEIGHT": 4, "OBSTACLE_RATIO": 1.0}
        settings.update(kwargs)
        return self.GENERATOR_CLASS(settings).get_game_state(DummyAvatarManager())

    def get_map(self, **kwargs):
        return self.get_game_state(**kwargs).world_map


class TestMainGenerator(_BaseGeneratorTestCase):
    GENERATOR_CLASS = map_generator.Main

    def test_map_dimensions(self):
        m = self.get_map()
        grid = list(m.all_cells())
        assert len(set(grid)) == len(grid), "Repeats in list"
        for c in grid:
            assert c.location.x <= 1
            assert c.location.y <= 2
            assert c.location.x >= -1
            assert c.location.y >= -1

    def test_obstacle_ratio(self):
        m = self.get_map(OBSTACLE_RATIO=0)
        obstacle_cells = [cell for cell in m.all_cells() if not cell.habitable]
        assert len(obstacle_cells) == 0

    def test_map_contains_some_non_habitable_cell(self):
        m = self.get_map()
        obstacle_cells = [cell for cell in m.all_cells() if not cell.habitable]
        assert len(obstacle_cells) >= 1

    def test_map_contains_some_habitable_cell_on_border(self):
        m = self.get_map(START_WIDTH=4)
        edge_coordinates = [
            (-1, 2),
            (0, 2),
            (1, 2),
            (2, 2),
            (-1, 1),
            (2, 1),
            (-1, 0),
            (2, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
            (2, -1),
        ]
        edge_cells = (m.get_cell_by_coords(x, y) for (x, y) in edge_coordinates)
        habitable_edge_cells = [cell for cell in edge_cells if cell.habitable]

        assert len(habitable_edge_cells) >= 1

    def test_shortest_path(self):
        m = self.get_map(START_WIDTH=4)
