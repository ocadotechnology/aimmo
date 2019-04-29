from __future__ import absolute_import

import math
from string import ascii_uppercase
from unittest import TestCase

from simulation.game_logic import SpawnLocationFinder
from simulation.interactables.interactable import _Interactable
from simulation.interactables.pickups import ALL_PICKUPS, HealthPickup
from simulation.interactables.score_location import ScoreLocation
from simulation.location import Location
from simulation.world_map import WorldMap, WorldMapStaticSpawnDecorator

from .dummy_avatar import DummyAvatar
from .maps import AvatarMap, MockCell, MockPickup


def int_ceil(num):
    return int(math.ceil(num))


def int_floor(num):
    return int(math.floor(num))


class serializer(object):
    def __init__(self, content):
        self.content = content

    def serialize(self):
        return self.content


class TestWorldMap(TestCase):
    def setUp(self):
        self.settings = {
            "TARGET_NUM_CELLS_PER_AVATAR": 0,
            "TARGET_NUM_PICKUPS_PER_AVATAR": 0,
            "TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR": 0,
            "SCORE_DESPAWN_CHANCE": 0,
            "PICKUP_SPAWN_CHANCE": 0,
        }

    def _generate_grid(self, columns=2, rows=2):
        alphabet = iter(ascii_uppercase)
        grid = {
            Location(x, y): MockCell(Location(x, y), name=next(alphabet))
            for x in range(columns)
            for y in range(rows)
        }
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
        self.assertEqual(world_map.num_cells, expected_rows * expected_columns)
        self.assertEqual(
            len(list(world_map.all_cells())), expected_rows * expected_columns
        )

    def test_get_all_cells(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        cell_list = list(world_map.all_cells())

        self.assertEqual(len(cell_list), 4)
        self.assertTrue(isinstance(cell_list[0], MockCell))

    def test_get_all_interactables(self):
        interactable_cell = MockCell()
        interactable_cell.interactable = ScoreLocation(interactable_cell)
        grid = self._grid_from_list(
            [[interactable_cell, MockCell()], [MockCell(), MockCell()]]
        )
        world_map = WorldMap(grid, self.settings)
        interactable_list = list(world_map.interactable_cells())

        self.assertEqual(len(interactable_list), 1)
        self.assertTrue(isinstance(interactable_list[0].interactable, _Interactable))

    def test_get_all_score_locations(self):
        score_cell = MockCell()
        score_cell.interactable = ScoreLocation(score_cell)
        grid = self._grid_from_list(
            [[score_cell, MockCell()], [MockCell(), MockCell()]]
        )
        world_map = WorldMap(grid, self.settings)
        score_list = list(world_map.score_cells())

        self.assertEqual(len(score_list), 1)
        self.assertTrue(isinstance(score_list[0].interactable, ScoreLocation))

    def test_get_all_pickup_locations(self):
        pickup_cell = MockCell()
        pickup_cell.interactable = HealthPickup(pickup_cell)
        grid = self._grid_from_list(
            [[pickup_cell, MockCell()], [MockCell(), MockCell()]]
        )
        world_map = WorldMap(grid, self.settings)
        pickup_list = list(world_map.pickup_cells())

        self.assertEqual(len(pickup_list), 1)
        self.assertTrue(isinstance(pickup_list[0].interactable, ALL_PICKUPS))

    def test_grid_size(self):
        world_map = WorldMap(self._generate_grid(1, 3), self.settings)
        self.assertGridSize(world_map, 1, 3)

    def test_generated_map(self):
        world_map = WorldMap.generate_empty_map(2, 5, {})
        self.assertGridSize(world_map, 5, 2)

    def test_all_cells(self):
        world_map = WorldMap(self._generate_grid(), self.settings)
        cell_names = [c.name for c in world_map.all_cells()]
        self.assertIn("A", cell_names)
        self.assertIn("B", cell_names)
        self.assertIn("C", cell_names)
        self.assertIn("D", cell_names)
        self.assertEqual(len(cell_names), 4)

    def test_score_cells(self):
        score_cell1 = MockCell()
        score_cell1.interactable = ScoreLocation(score_cell1)
        score_cell2 = MockCell()
        score_cell2.interactable = ScoreLocation(score_cell2)
        no_score_cell = MockCell()
        grid = self._grid_from_list(
            [[score_cell1, no_score_cell], [no_score_cell, score_cell2]]
        )
        world_map = WorldMap(grid, self.settings)
        cells = list(world_map.score_cells())
        self.assertIn(score_cell1, cells)
        self.assertIn(score_cell2, cells)
        self.assertEqual(len(cells), 2, "Non-scoring cells present")

    def test_potential_spawns(self):
        spawnable1 = MockCell()
        spawnable2 = MockCell()
        score_cell = MockCell()
        score_cell.interactable = ScoreLocation(score_cell)
        unhabitable = MockCell(habitable=False)
        filled = MockCell(avatar="avatar")
        grid = self._grid_from_list(
            [[spawnable1, score_cell, unhabitable], [unhabitable, spawnable2, filled]]
        )
        world_map = WorldMap(grid, self.settings)
        spawn_location_finder = SpawnLocationFinder(world_map)
        cells = list(spawn_location_finder.potential_spawn_locations())
        self.assertIn(spawnable1, cells)
        self.assertIn(spawnable2, cells)
        self.assertNotIn(score_cell, cells, "Score cells should not be spawns")
        self.assertNotIn(unhabitable, cells, "Unhabitable cells should not be spawns")
        self.assertNotIn(filled, cells, "Cells with avatars should not be spawns")
        self.assertEqual(len(cells), 2)

    def test_interactable_cells(self):
        pickup_cell1 = MockCell(interactable=MockPickup())
        pickup_cell2 = MockCell(interactable=MockPickup())
        no_pickup_cell = MockCell()
        grid = self._grid_from_list(
            [[pickup_cell1, no_pickup_cell], [no_pickup_cell, pickup_cell2]]
        )
        world_map = WorldMap(grid, self.settings)
        cells = list(world_map.interactable_cells())
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
            [
                MockCell(Location(-1, -1), name="A"),
                MockCell(Location(-1, 0), name="B"),
                MockCell(Location(-1, 1), name="C"),
            ],
            [
                MockCell(Location(0, -1), name="D"),
                MockCell(Location(0, 0), name="E"),
                MockCell(Location(0, 1), name="F"),
            ],
            [
                MockCell(Location(1, -1), name="E"),
                MockCell(Location(1, 0), name="G"),
                MockCell(Location(1, 1), name="H"),
            ],
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
        grid = {
            Location(x, y): MockCell(Location(x, y), name=next(alphabet))
            for x in range(-int_ceil(columns / 2.0) + 1, int_floor(columns / 2.0) + 1)
            for y in range(-int_ceil(rows / 2.0) + 1, int_floor(rows / 2.0) + 1)
        }

        return grid

    def _grid_from_list(self, in_list):
        out = {}
        min_x = -int_ceil(len(in_list) / 2.0) + 1
        min_y = -int_ceil(len(in_list[0]) / 2.0) + 1
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
