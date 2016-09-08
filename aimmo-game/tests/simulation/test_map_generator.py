from __future__ import absolute_import
import unittest
from simulation import map_generator
from simulation.map_generator import get_random_edge_index
from simulation.location import Location
from .dummy_avatar import DummyAvatarManager


class ConstantRng(object):

    def __init__(self, value):
        self.value = value

    def randint(self, minimum, maximum):
        if not minimum <= self.value <= maximum:
            raise ValueError('Beyond range')
        return self.value


class TestHelperFunctions(unittest.TestCase):
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


class _BaseGeneratorTestCase(unittest.TestCase):
    def get_game_state(self, **kwargs):
        settings = {
            'START_WIDTH': 3,
            'START_HEIGHT': 4,
            'OBSTACLE_RATIO': 1.0
        }
        settings.update(kwargs)
        return self.GENERATOR_CLASS(settings).get_game_state(DummyAvatarManager())

    def get_map(self, **kwargs):
        return self.get_game_state(**kwargs).world_map


class TestMainGenerator(_BaseGeneratorTestCase):
    GENERATOR_CLASS = map_generator.Main

    def test_map_dimensions(self):
        m = self.get_map()
        grid = list(m.all_cells())
        self.assertEqual(len(set(grid)), len(grid), "Repeats in list")
        for c in grid:
            self.assertLess(c.location.x, 3)
            self.assertLess(c.location.y, 4)
            self.assertGreaterEqual(c.location.x, 0)
            self.assertGreaterEqual(c.location.y, 0)

    def test_obstable_ratio(self):
        m = self.get_map(OBSTACLE_RATIO=0)
        obstacle_cells = [cell for row in m.grid for cell in row if not cell.habitable]
        self.assertEqual(len(obstacle_cells), 0)

    def test_map_contains_some_non_habitable_cell(self):
        m = self.get_map()
        obstacle_cells = [cell for row in m.grid for cell in row if not cell.habitable]
        self.assertGreaterEqual(len(obstacle_cells), 1)

    def test_map_contains_some_habitable_cell_on_border(self):
        m = self.get_map(START_WIDTH=4)
        edge_coordinates = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (3, 1),
            (0, 2), (3, 2),
            (0, 3), (1, 3), (2, 3), (3, 3)
        ]
        edge_cells = (m.get_cell(Location(x, y)) for (x, y) in edge_coordinates)
        habitable_edge_cells = [cell for cell in edge_cells if cell.habitable]

        self.assertGreaterEqual(len(habitable_edge_cells), 1)

    def test_not_complete(self):
        game_state = self.get_game_state()
        self.assertFalse(game_state.is_complete())


class TestLevel1Generator(_BaseGeneratorTestCase):
    GENERATOR_CLASS = map_generator.Level1

    def test_width_5(self):
        self.assertEqual(self.get_map().num_cols, 5)

    def test_height_1(self):
        self.assertEqual(self.get_map().num_rows, 1)

    def test_incomplete_without_avatars(self):
        game_state = self.get_game_state()
        self.assertFalse(game_state.is_complete())

    def test_incomplete_at_score_0(self):
        game_state = self.get_game_state()
        game_state.avatar_manager.add_avatar(1, '', None)
        game_state.main_avatar_id = 1
        self.assertFalse(game_state.is_complete())

    def test_completes_at_score_1(self):
        game_state = self.get_game_state()
        game_state.avatar_manager.add_avatar(1, '', None)
        game_state.avatar_manager.avatars_by_id[1].score = 1
        game_state.main_avatar_id = 1
        self.assertTrue(game_state.is_complete())

    def test_static_spawn(self):
        game_state = self.get_game_state()
        for i in xrange(5):
            game_state.add_avatar(i, '')
            self.assertEqual(game_state.avatar_manager.avatars_by_id[i].location, Location(0, 0))
