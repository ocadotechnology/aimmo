from __future__ import absolute_import

import math
from string import ascii_uppercase
from unittest import TestCase

from simulation.location import Location
from simulation.world_map import WorldMap, WorldMapStaticSpawnDecorator
from simulation.game_logic import SpawnLocationFinder
from .dummy_avatar import DummyAvatar
from .maps import MockCell, MockPickup, AvatarMap


def int_ceil(num):
    return int(math.ceil(num))


def int_floor(num):
    return int(math.floor(num))


class Serialiser(object):
    def __init__(self, content):
        self.content = content

    def serialise(self):
        return self.content


class TestWorldMap(TestCase):
    def setUp(self):
        self.settings = {
            'TARGET_NUM_CELLS_PER_AVATAR': 0,
            'TARGET_NUM_PICKUPS_PER_AVATAR': 0,
            'TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR': 0,
            'SCORE_DESPAWN_CHANCE': 0,
            'PICKUP_SPAWN_CHANCE': 0,
        }

    def _generate_grid(self, columns=2, rows=2):
        alphabet = iter(ascii_uppercase)
        grid = {Location(x, y): MockCell(Location(x, y), name=next(alphabet))
                for x in range(columns) for y in range(rows)}
        return grid

    def _grid_from_list(self, in_list):
        out = {}
        for x, column in enumerate(in_list):
            for y, cell in enumerate(column):
                out[Location(x, y)] = cell
        return out

    def assertGridSize(self, world_map, expected_columns, expected_rows=None):
        if expected_rows is None:
            expected_rows = expected_columns
        self.assertEqual(world_map.num_rows, expected_rows)
        self.assertEqual(world_map.num_cols, expected_columns)
        self.assertEqual(world_map.num_cells, expected_rows*expected_columns)
        self.assertEqual(len(list(world_map.all_cells())), expected_rows*expected_columns)

    def test_grid_size(self):
        world_map = WorldMap(self._generate_grid(1, 3), self.settings)
        self.assertGridSize(world_map, 1, 3)

    def test_generated_map(self):
        world_map = WorldMap.generate_empty_map(2, 5, {})
        self.assertGridSize(world_map, 5, 2)

    def test_all_cells(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        cell_names = [c.name for c in world_map.all_cells()]
        self.assertIn('A', cell_names)
        self.assertIn('B', cell_names)
        self.assertIn('C', cell_names)
        self.assertIn('D', cell_names)
        self.assertEqual(len(cell_names), 4)

    def test_score_cells(self):
        score_cell1 = MockCell(generates_score=True)
        score_cell2 = MockCell(generates_score=True)
        no_score_cell = MockCell()
        grid = self._grid_from_list([[score_cell1, no_score_cell],
                                     [no_score_cell, score_cell2]])
        world_map = WorldMap(grid, self.settings)
        cells = list(world_map.score_cells())
        self.assertIn(score_cell1, cells)
        self.assertIn(score_cell2, cells)
        self.assertEqual(len(cells), 2, "Non-scoring cells present")

    def test_potential_spawns(self):
        spawnable1 = MockCell()
        spawnable2 = MockCell()
        score_cell = MockCell(generates_score=True)
        unhabitable = MockCell(habitable=False)
        filled = MockCell(avatar='avatar')
        grid = self._grid_from_list([[spawnable1, score_cell, unhabitable],
                                     [unhabitable, spawnable2, filled]])
        world_map = WorldMap(grid, self.settings)
        spawn_location_finder = SpawnLocationFinder(world_map)
        cells = list(spawn_location_finder.potential_spawn_locations())
        self.assertIn(spawnable1, cells)
        self.assertIn(spawnable2, cells)
        self.assertNotIn(score_cell, cells, "Score cells should not be spawns")
        self.assertNotIn(unhabitable, cells, "Unhabitable cells should not be spawns")
        self.assertNotIn(filled, cells, "Cells with avatars should not be spawns")
        self.assertEqual(len(cells), 2)

    def test_pickup_cells(self):
        pickup_cell1 = MockCell(pickup=MockPickup())
        pickup_cell2 = MockCell(pickup=MockPickup())
        no_pickup_cell = MockCell()
        grid = self._grid_from_list([[pickup_cell1, no_pickup_cell],
                                     [no_pickup_cell, pickup_cell2]])
        world_map = WorldMap(grid, self.settings)
        cells = list(world_map.pickup_cells())
        self.assertIn(pickup_cell1, cells)
        self.assertIn(pickup_cell2, cells)
        self.assertEqual(len(cells), 2, "Non-pickup cells present")

    def test_location_on_map(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        for x in (0, 1):
            for y in (0, 1):
                self.assertTrue(world_map.is_on_map(Location(x, y)))

        self.assertFalse(world_map.is_on_map(Location(2, 2)))
        self.assertFalse(world_map.is_on_map(Location(-1, 1)))

    def test_x_off_map(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        for y in (0, 1):
            self.assertFalse(world_map.is_on_map(Location(-1, y)))
            self.assertFalse(world_map.is_on_map(Location(2, y)))

    def test_y_off_map(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        for x in (0, 1):
            self.assertFalse(world_map.is_on_map(Location(x, -1)))
            self.assertFalse(world_map.is_on_map(Location(x, 2)))

    def test_get_valid_cell(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        for x in (0, 1):
            for y in (0, 1):
                location = Location(x, y)
                self.assertEqual(world_map.get_cell(location).location, location)

    def test_get_x_off_map(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        for y in (0, 1):
            with self.assertRaises(ValueError):
                world_map.get_cell(Location(-1, y))
            with self.assertRaises(ValueError):
                world_map.get_cell(Location(2, y))

    def test_get_y_off_map(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        for x in (0, 1):
            with self.assertRaises(ValueError):
                world_map.get_cell(Location(x, -1))
            with self.assertRaises(ValueError):
                world_map.get_cell(Location(x, 2))

    def test_grid_expand(self):
        self.settings['TARGET_NUM_CELLS_PER_AVATAR'] = 5
        world_map = WorldMap(self._generate_grid(), self.settings)
        world_map.update(1)
        self.assertTrue(world_map.is_on_map(Location(-1, -1)))
        self.assertTrue(world_map.is_on_map(Location(-1, 2)))
        self.assertTrue(world_map.is_on_map(Location(2, 2)))
        self.assertTrue(world_map.is_on_map(Location(2, -1)))
        self.assertGridSize(world_map, 4)
        world_map.update(4)
        self.assertGridSize(world_map, 6)
        self.assertTrue(world_map.is_on_map(Location(0, 3)))
        self.assertTrue(world_map.is_on_map(Location(3, 0)))
        self.assertTrue(world_map.is_on_map(Location(-2, 0)))
        self.assertTrue(world_map.is_on_map(Location(0, -2)))

    def test_grid_doesnt_expand(self):
        self.settings['TARGET_NUM_CELLS_PER_AVATAR'] = 4
        world_map = WorldMap(self._generate_grid(), self.settings)
        world_map.update(1)
        self.assertGridSize(world_map, 2)

    def test_scores_removed(self):
        self.settings['SCORE_DESPAWN_CHANCE'] = 1
        grid = self._generate_grid()
        grid[Location(0, 1)].generates_score = True
        world_map = WorldMap(grid, self.settings)
        world_map.update(1)
        self.assertEqual(len(list(world_map.score_cells())), 0)

    def test_score_despawn_chance(self):
        self.settings['TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR'] = 0
        grid = self._generate_grid()
        grid[Location(0, 1)].generates_score = True
        world_map = WorldMap(grid, self.settings)
        world_map.update(1)
        self.assertIn(grid[Location(0, 1)], world_map.score_cells())
        self.assertEqual(len(list(world_map.score_cells())), 1)

    def test_scores_added(self):
        self.settings['TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR'] = 1
        world_map = WorldMap(self._generate_grid(), self.settings)
        world_map.update(1)
        self.assertEqual(len(list(world_map.score_cells())), 1)

        world_map.update(2)
        self.assertEqual(len(list(world_map.score_cells())), 2)

    def test_scores_applied(self):
        grid = self._generate_grid()
        avatar = DummyAvatar()
        grid[Location(1, 1)].generates_score = True
        grid[Location(1, 1)].avatar = avatar
        WorldMap(grid, self.settings).update(1)
        self.assertEqual(avatar.score, 1)

    def test_scores_not_added_when_at_target(self):
        self.settings['TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR'] = 1
        grid = self._generate_grid()
        grid[Location(0, 1)].generates_score = True
        world_map = WorldMap(grid, self.settings)
        world_map.update(1)
        self.assertEqual(len(list(world_map.score_cells())), 1)
        self.assertIn(grid[Location(0, 1)], world_map.score_cells())

    def test_not_enough_score_space(self):
        self.settings['TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR'] = 1
        grid = self._generate_grid(1, 1)
        grid[Location(0, 0)].avatar = 'avatar'
        world_map = WorldMap(grid, self.settings)
        world_map.update(1)
        self.assertEqual(len(list(world_map.score_cells())), 0)

    def test_pickups_added(self):
        self.settings['TARGET_NUM_PICKUPS_PER_AVATAR'] = 1
        self.settings['PICKUP_SPAWN_CHANCE'] = 1
        world_map = WorldMap(self._generate_grid(), self.settings)
        world_map.update(1)
        self.assertEqual(len(list(world_map.pickup_cells())), 1)

        world_map.update(2)
        self.assertEqual(len(list(world_map.pickup_cells())), 2)

    def test_pickups_applied(self):
        grid = self._generate_grid()
        pickup = MockPickup()
        avatar = DummyAvatar()
        grid[Location(1, 1)].pickup = pickup
        grid[Location(1, 1)].avatar = avatar
        WorldMap(grid, self.settings).update(1)
        self.assertEqual(pickup.applied_to, avatar)

    def test_pickup_spawn_chance(self):
        self.settings['TARGET_NUM_PICKUPS_PER_AVATAR'] = 5
        self.settings['PICKUP_SPAWN_CHANCE'] = 0
        grid = self._generate_grid()
        world_map = WorldMap(grid, self.settings)
        world_map.update(1)
        self.assertEqual(len(list(world_map.pickup_cells())), 0)

    def test_pickups_not_added_when_at_target(self):
        self.settings['TARGET_NUM_PICKUPS_PER_AVATAR'] = 1
        grid = self._generate_grid()
        grid[Location(0, 1)].pickup = MockPickup()
        world_map = WorldMap(grid, self.settings)
        world_map.update(1)
        self.assertEqual(len(list(world_map.pickup_cells())), 1)
        self.assertIn(grid[Location(0, 1)], world_map.pickup_cells())

    def test_not_enough_pickup_space(self):
        self.settings['TARGET_NUM_PICKUPS_PER_AVATAR'] = 1
        grid = self._generate_grid(1, 1)
        grid[Location(0, 0)].generates_score = True
        world_map = WorldMap(grid, self.settings)
        world_map.update(1)
        self.assertEqual(len(list(world_map.pickup_cells())), 0)

    def test_random_spawn_location_successful(self):
        cell = MockCell()
        world_map = WorldMap({Location(0, 0): cell}, self.settings)
        self.assertEqual(world_map.get_random_spawn_location(), cell.location)

    def test_random_spawn_location_with_no_candidates(self):
        grid = self._generate_grid(1, 1)
        world_map = WorldMap(grid, self.settings)
        grid[Location(0, 0)].avatar = True
        with self.assertRaises(IndexError):
            world_map.get_random_spawn_location()

    def test_can_move_to(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        target = Location(1, 1)
        self.assertTrue(world_map.can_move_to(target))

    def test_cannot_move_to_cell_off_grid(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        target = Location(4, 1)
        self.assertFalse(world_map.can_move_to(target))

    def test_cannot_move_to_uninhabitable_cell(self):
        target = Location(0, 0)
        cell = MockCell(target, habitable=False)
        world_map = WorldMap({target: cell}, self.settings)
        self.assertFalse(world_map.can_move_to(target))

    def test_cannot_move_to_habited_cell(self):
        target = Location(0, 0)
        cell = MockCell(target, avatar=DummyAvatar(target, 0))
        world_map = WorldMap({target: cell}, self.settings)
        target = Location(0, 0)
        self.assertFalse(world_map.can_move_to(target))

    def test_empty_grid(self):
        world_map = WorldMap({}, self.settings)
        self.assertFalse(world_map.is_on_map(Location(0, 0)))

    def test_iter(self):
        grid = [
            [MockCell(Location(-1, -1), name='A'), MockCell(Location(-1, 0), name='B'), MockCell(Location(-1, 1), name='C')],
            [MockCell(Location(0, -1), name='D'), MockCell(Location(0, 0), name='E'), MockCell(Location(0, 1), name='F')],
            [MockCell(Location(1, -1), name='E'), MockCell(Location(1, 0), name='G'), MockCell(Location(1, 1), name='H')],
        ]
        world_map = WorldMap(self._grid_from_list(grid), self.settings)
        self.assertEqual([list(column) for column in world_map], grid)

    def test_attackable_avatar_returns_none(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        for x in (0, 1):
            for y in (0, 1):
                self.assertIsNone(world_map.attackable_avatar(Location(x, y)))

    def test_attackable_avatar_returns_avatar(self):
        avatar = DummyAvatar()
        world_map = AvatarMap(avatar)

        self.assertEqual(world_map.attackable_avatar(Location(0, 0)), avatar)


class TestWorldMapWithOriginCentre(TestWorldMap):
    def _generate_grid(self, columns=2, rows=2):
        alphabet = iter(ascii_uppercase)
        grid = {Location(x, y): MockCell(Location(x, y), name=next(alphabet))
                for x in range(-int_ceil(columns/2.0)+1, int_floor(columns/2.0)+1) for y in range(-int_ceil(rows/2.0)+1, int_floor(rows/2.0)+1)}

        return grid

    def _grid_from_list(self, in_list):
        out = {}
        min_x = -int_ceil(len(in_list)/2.0) + 1
        min_y = -int_ceil(len(in_list[0])/2.0) + 1
        for i, column in enumerate(in_list):
            x = i + min_x
            for j, cell in enumerate(column):
                y = j + min_y
                out[Location(x, y)] = cell
        return out

    def test_retrieve_negative(self):
        world_map = WorldMap(self._generate_grid(3, 3), self.settings)
        self.assertTrue(world_map.is_on_map(Location(-1, -1)))


class TestStaticSpawnDecorator(TestCase):
    def test_spawn_is_static(self):
        decorated_map = WorldMapStaticSpawnDecorator(WorldMap({}, {}), Location(3, 7))
        for _ in range(5):
            self.assertEqual(decorated_map.get_random_spawn_location(), Location(3, 7))
