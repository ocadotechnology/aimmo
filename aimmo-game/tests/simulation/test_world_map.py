from __future__ import absolute_import

from string import ascii_uppercase
import unittest
from unittest import TestCase

from simulation import world_map
from simulation.direction import NORTH
from simulation.direction import EAST
from simulation.direction import SOUTH
from simulation.direction import WEST
from simulation.location import Location
from simulation.world_map import Cell, WorldMap

from .maps import MockCell
from .dummy_avatar import DummyAvatar

ORIGIN = Location(x=0, y=0)


class Serialiser(object):
    def __init__(self, content):
        self.content = content

    def serialise(self):
        return self.content


class TestCell(TestCase):
    def test_equal(self):
        cell1 = Cell(ORIGIN)
        cell2 = Cell(ORIGIN)
        self.assertEqual(cell1, cell2)

    def test_not_equal(self):
        cell1 = Cell(ORIGIN)
        cell2 = Cell(ORIGIN + EAST)
        self.assertNotEqual(cell1, cell2)

    def _create_full_cell(self):
        cell = Cell(Serialiser('location'), False, True)
        cell.pickup = Serialiser('pickup')
        self.expected = {
            'avatar': None,
            'generates_score': True,
            'habitable': False,
            'location': 'location',
            'pickup': 'pickup',
            'partially_fogged': False
        }
        return cell

    def test_serialise(self):
        cell = self._create_full_cell()
        self.assertEqual(cell.serialise(), self.expected)

    def test_serialise_no_avatar(self):
        cell = self._create_full_cell()
        cell.avatar = None
        self.expected['avatar'] = None
        self.assertEqual(cell.serialise(), self.expected)

    def test_serialise_no_pickup(self):
        cell = self._create_full_cell()
        cell.pickup = None
        self.expected['pickup'] = None
        self.assertEqual(cell.serialise(), self.expected)


class TestWorldMap(TestCase):
    def setUp(self):
        world_map.TARGET_NUM_CELLS_PER_AVATAR = 0
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 0
        world_map.TARGET_NUM_SCORE_CELLS_PER_AVATAR = 0
        world_map.SCORE_DESPAWN_CHANCE = 0
        world_map.PICKUP_SPAWN_CHANCE = 0

    def _generate_grid(self, columns=2, rows=2):
        alphabet = iter(ascii_uppercase)
        grid = []
        for x in xrange(columns):
            column = []
            for y in xrange(rows):
                column.append(MockCell(Location(x, y), name=next(alphabet)))
            grid.append(column)
        return grid

    def assertGridSize(self, map, expected_rows, expected_columns=None):
        if expected_columns is None:
            expected_columns = expected_rows
        self.assertEqual(map.num_cols, expected_rows)
        self.assertEqual(map.num_rows, expected_columns)
        self.assertEqual(len(list(map.all_cells)), expected_rows * expected_columns)

    def test_grid_size(self):
        map = WorldMap(self._generate_grid(1, 3))
        self.assertGridSize(map, 1, 3)

    def test_all_cells(self):
        map = WorldMap(self._generate_grid())
        cell_names = [c.name for c in map.all_cells]
        self.assertIn('A', cell_names)
        self.assertIn('B', cell_names)
        self.assertIn('C', cell_names)
        self.assertIn('D', cell_names)
        self.assertEqual(len(cell_names), 4)

    def test_score_cells(self):
        score_cell1 = MockCell(generates_score=True)
        score_cell2 = MockCell(generates_score=True)
        no_score_cell = MockCell()
        grid = [[score_cell1, no_score_cell], [no_score_cell, score_cell2]]
        map = WorldMap(grid)
        cells = list(map.score_cells)
        self.assertIn(score_cell1, cells)
        self.assertIn(score_cell2, cells)
        self.assertEqual(len(cells), 2, "Non-scoring cells present")

    def test_potential_spawns(self):
        spawnable1 = MockCell()
        spawnable2 = MockCell()
        score_cell = MockCell(generates_score=True)
        unhabitable = MockCell(habitable=False)
        filled = MockCell(avatar='avatar')
        grid = [[spawnable1, score_cell, unhabitable], [unhabitable, spawnable2, filled]]
        map = WorldMap(grid)
        cells = list(map._potential_spawn_cells())
        self.assertIn(spawnable1, cells)
        self.assertIn(spawnable2, cells)
        self.assertNotIn(score_cell, cells, "Score cells should not be spawns")
        self.assertNotIn(unhabitable, cells, "Unhabitable cells should not be spawns")
        self.assertNotIn(filled, cells, "Cells with avatars should not be spawns")
        self.assertEqual(len(cells), 2)

    def test_pickup_cells(self):
        pickup_cell1 = MockCell(pickup='pickup1')
        pickup_cell2 = MockCell(pickup='pickup')
        no_pickup_cell = MockCell()
        grid = [[pickup_cell1, no_pickup_cell], [no_pickup_cell, pickup_cell2]]
        map = WorldMap(grid)
        cells = list(map.pickup_cells)
        self.assertIn(pickup_cell1, cells)
        self.assertIn(pickup_cell2, cells)
        self.assertEqual(len(cells), 2, "Non-pickup cells present")

    def test_location_on_map(self):
        map = WorldMap(self._generate_grid())
        for x in (0, 1):
            for y in (0, 1):
                self.assertTrue(map.location_on_map(Location(x, y)))

    def test_x_off_map(self):
        map = WorldMap(self._generate_grid())
        for y in (0, 1):
            self.assertFalse(map.location_on_map(Location(-1, y)))
            self.assertFalse(map.location_on_map(Location(2, y)))

    def test_y_off_map(self):
        map = WorldMap(self._generate_grid())
        for x in (0, 1):
            self.assertFalse(map.location_on_map(Location(x, -1)))
            self.assertFalse(map.location_on_map(Location(x, 2)))

    def test_get_valid_cell(self):
        map = WorldMap(self._generate_grid())
        for x in (0, 1):
            for y in (0, 1):
                location = Location(x, y)
                self.assertEqual(map.get_cell(location).location, location)

    def test_get_x_off_map(self):
        map = WorldMap(self._generate_grid())
        for y in (0, 1):
            with self.assertRaises(ValueError):
                map.get_cell(Location(-1, y))
            with self.assertRaises(ValueError):
                map.get_cell(Location(2, y))

    def test_get_y_off_map(self):
        map = WorldMap(self._generate_grid())
        for x in (0, 1):
            with self.assertRaises(ValueError):
                map.get_cell(Location(x, -1))
            with self.assertRaises(ValueError):
                map.get_cell(Location(x, 2))

    def test_grid_expand(self):
        world_map.TARGET_NUM_CELLS_PER_AVATAR = 5
        map = WorldMap(self._generate_grid())
        map.expand(1)
        self.assertGridSize(map, 3)

        map.expand(2)
        self.assertGridSize(map, 4)

    def test_grid_doesnt_expand(self):
        world_map.TARGET_NUM_CELLS_PER_AVATAR = 4
        map = WorldMap(self._generate_grid())
        map.expand(1)
        self.assertGridSize(map, 2)

    def test_scores_removed(self):
        world_map.SCORE_DESPAWN_CHANCE = 1
        grid = self._generate_grid()
        grid[0][1].generates_score = True
        map = WorldMap(grid)
        map.reset_score_locations(1)
        self.assertEqual(len(list(map.score_cells)), 0)

    def test_score_despawn_chance(self):
        world_map.TARGET_NUM_SCORE_CELLS_PER_AVATAR = 0
        grid = self._generate_grid()
        grid[0][1].generates_score = True
        map = WorldMap(grid)
        map.reset_score_locations(1)
        self.assertIn(grid[0][1], map.score_cells)
        self.assertEqual(len(list(map.score_cells)), 1)

    def test_scores_added(self):
        world_map.TARGET_NUM_SCORE_CELLS_PER_AVATAR = 1
        map = WorldMap(self._generate_grid())
        map.reset_score_locations(1)
        self.assertEqual(len(list(map.score_cells)), 1)

        map.reset_score_locations(2)
        self.assertEqual(len(list(map.score_cells)), 2)

    def test_scores_not_added_when_at_target(self):
        world_map.TARGET_NUM_SCORE_CELLS_PER_AVATAR = 1
        grid = self._generate_grid()
        grid[0][1].generates_score = True
        map = WorldMap(grid)
        map.reset_score_locations(1)
        self.assertEqual(len(list(map.score_cells)), 1)
        self.assertIn(grid[0][1], map.score_cells)

    def test_not_enough_score_space(self):
        world_map.TARGET_NUM_SCORE_CELLS_PER_AVATAR = 1
        grid = self._generate_grid(1)
        grid = [[MockCell(avatar='avatar')]]
        map = WorldMap(grid)
        map.reset_score_locations(1)
        self.assertEqual(len(list(map.score_cells)), 0)

    def test_pickups_added(self):
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 1
        world_map.PICKUP_SPAWN_CHANCE = 1
        map = WorldMap(self._generate_grid())
        map.add_pickups(1)
        self.assertEqual(len(list(map.pickup_cells)), 1)

        map.add_pickups(2)
        self.assertEqual(len(list(map.pickup_cells)), 2)

    def test_pickup_spawn_chance(self):
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 5
        world_map.PICKUP_SPAWN_CHANCE = 0
        grid = self._generate_grid()
        map = WorldMap(grid)
        map.add_pickups(1)
        self.assertEqual(len(list(map.pickup_cells)), 0)

    def test_pickups_not_added_when_at_target(self):
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 1
        grid = self._generate_grid()
        grid[0][1].pickup = True
        map = WorldMap(grid)
        map.add_pickups(1)
        self.assertEqual(len(list(map.pickup_cells)), 1)
        self.assertIn(grid[0][1], map.pickup_cells)

    def test_not_enough_pickup_space(self):
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 1
        grid = self._generate_grid(1)
        grid = [[MockCell(avatar='avatar')]]
        map = WorldMap(grid)
        map.add_pickups(1)
        self.assertEqual(len(list(map.pickup_cells)), 0)

    def test_random_spawn_location(self):
        cell = MockCell()
        map = WorldMap([[cell]])
        self.assertEqual(map.get_random_spawn_location(), cell.location)

    def test_random_spawn_location_with_no_candidates(self):
        cell = MockCell()
        map = WorldMap([[cell]])
        cell.avatar = 'true'
        with self.assertRaises(IndexError):
            map.get_random_spawn_location()

    @unittest.skip("Responsibility for checking legality moved to action code.")
    def test_can_move_to(self):
        map = WorldMap(self._generate_grid())
        target = Location(1, 1)
        self.assertTrue(map.can_move_to(target))

    @unittest.skip("Responsibility for checking legality moved to action code.")
    def test_cannot_move_to_cell_off_grid(self):
        map = WorldMap(self._generate_grid())
        target = Location(4, 1)
        self.assertFalse(map.can_move_to(target))

    @unittest.skip("Responsibility for checking legality moved to action code.")
    def test_cannot_move_to_uninhabitable_cell(self):
        target = Location(0, 0)
        cell = MockCell(target, habitable=False)
        map = WorldMap([[cell]])
        self.assertFalse(map.can_move_to(target))

    @unittest.skip("Responsibility for checking legality moved to action code.")
    def test_cannot_move_to_habited_cell(self):
        target = Location(0, 0)
        cell = MockCell(target, avatar=DummyAvatar(target, 0))
        map = WorldMap([[cell]])
        target = Location(0, 0)
        self.assertFalse(map.can_move_to(target))
