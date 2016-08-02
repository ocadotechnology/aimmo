from __future__ import absolute_import

from string import ascii_uppercase
from unittest import TestCase

from simulation import world_map
from simulation.location import Location
from simulation.world_map import Cell, WorldMap

from .maps import MockCell
from .dummy_avatar import DummyAvatar


class Serialiser(object):
    def __init__(self, content):
        self.content = content

    def serialise(self):
        return self.content


class TestCell(TestCase):
    def test_equal(self):
        cell1 = Cell(1)
        cell2 = Cell(1)
        self.assertEqual(cell1, cell2)

    def test_not_equal(self):
        cell1 = Cell(1)
        cell2 = Cell(2)
        self.assertNotEqual(cell1, cell2)

    def _create_full_cell(self):
        cell = Cell(Serialiser('location'), False, True)
        cell.avatar = Serialiser('avatar')
        cell.pickup = Serialiser('pickup')
        self.expected = {
            'avatar': 'avatar',
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
        world_map.TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 0
        world_map.SCORE_DESPAWN_CHANCE = 0
        world_map.PICKUP_SPAWN_CHANCE = 0

    def _generate_grid(self, columns=2, rows=2):
        alphabet = iter(ascii_uppercase)
        grid = {Location(x, y): MockCell(Location(x, y), name=next(alphabet))
                for x in xrange(columns) for y in xrange(rows)}
        return grid

    def _generate_list_grid(self, columns=2, rows=2):
        alphabet = iter(ascii_uppercase)
        grid = []
        for x in xrange(columns):
            column = []
            for y in xrange(rows):
                column.append(MockCell(Location(x, y), name=next(alphabet)))
            grid.append(column)
        return grid

    def _grid_from_list(self, in_list):
        out = {}
        for x, column in enumerate(in_list):
            for y, cell in enumerate(column):
                out[Location(x, y)] = cell
        return out

    def assertGridSize(self, map, expected_columns, expected_rows=None):
        if expected_rows is None:
            expected_rows = expected_columns
        self.assertEqual(map.num_rows, expected_rows)
        self.assertEqual(map.num_cols, expected_columns)
        self.assertEqual(map.num_cells, expected_rows*expected_columns)
        self.assertEqual(len(list(map.all_cells())), expected_rows*expected_columns)

    def test_grid_size_from_dict(self):
        map = WorldMap(self._generate_grid(1, 3))
        self.assertGridSize(map, 1, 3)

    def test_grid_from_list_size(self):
        map = WorldMap(self._generate_list_grid(1, 3))
        self.assertGridSize(map, 1, 3)

    def test_generated_map(self):
        map = WorldMap.generate_empty_map(2, 5)
        self.assertGridSize(map, 5, 2)

    def test_all_cells_from_dict(self):
        map = WorldMap(self._generate_grid())
        cell_names = [c.name for c in map.all_cells()]
        self.assertIn('A', cell_names)
        self.assertIn('B', cell_names)
        self.assertIn('C', cell_names)
        self.assertIn('D', cell_names)
        self.assertEqual(len(cell_names), 4)

    def test_all_cells_from_list(self):
        map = WorldMap(self._generate_list_grid())
        cell_names = [c.name for c in map.all_cells()]
        self.assertIn('A', cell_names)
        self.assertIn('B', cell_names)
        self.assertIn('C', cell_names)
        self.assertIn('D', cell_names)
        self.assertEqual(len(cell_names), 4)

    def test_score_cells(self):
        score_cell1 = MockCell(generates_score=True)
        score_cell2 = MockCell(generates_score=True)
        no_score_cell = MockCell()
        grid = self._grid_from_list([[score_cell1, no_score_cell], [no_score_cell, score_cell2]])
        map = WorldMap(grid)
        cells = list(map.score_cells())
        self.assertIn(score_cell1, cells)
        self.assertIn(score_cell2, cells)
        self.assertEqual(len(cells), 2, "Non-scoring cells present")

    def test_potential_spawns(self):
        spawnable1 = MockCell()
        spawnable2 = MockCell()
        score_cell = MockCell(generates_score=True)
        unhabitable = MockCell(habitable=False)
        filled = MockCell(avatar='avatar')
        grid = self._grid_from_list([[spawnable1, score_cell, unhabitable], [unhabitable, spawnable2, filled]])
        map = WorldMap(grid)
        cells = list(map.potential_spawn_locations())
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
        grid = self._grid_from_list([[pickup_cell1, no_pickup_cell], [no_pickup_cell, pickup_cell2]])
        map = WorldMap(grid)
        cells = list(map.pickup_cells())
        self.assertIn(pickup_cell1, cells)
        self.assertIn(pickup_cell2, cells)
        self.assertEqual(len(cells), 2, "Non-pickup cells present")

    def test_location_on_map(self):
        map = WorldMap(self._generate_grid())
        for x in (0, 1):
            for y in (0, 1):
                self.assertTrue(map.is_on_map(Location(x, y)))

    def test_x_off_map(self):
        map = WorldMap(self._generate_grid())
        for y in (0, 1):
            self.assertFalse(map.is_on_map(Location(-1, y)))
            self.assertFalse(map.is_on_map(Location(2, y)))

    def test_y_off_map(self):
        map = WorldMap(self._generate_grid())
        for x in (0, 1):
            self.assertFalse(map.is_on_map(Location(x, -1)))
            self.assertFalse(map.is_on_map(Location(x, 2)))

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
        map.reconstruct_interactive_state(1)
        self.assertTrue(map.is_on_map(Location(-1, -1)))
        self.assertTrue(map.is_on_map(Location(-1, 2)))
        self.assertTrue(map.is_on_map(Location(2, 2)))
        self.assertTrue(map.is_on_map(Location(2, -1)))
        self.assertGridSize(map, 4)
        map.reconstruct_interactive_state(4)
        self.assertGridSize(map, 6)
        self.assertTrue(map.is_on_map(Location(0, 3)))
        self.assertTrue(map.is_on_map(Location(3, 0)))
        self.assertTrue(map.is_on_map(Location(-2, 0)))
        self.assertTrue(map.is_on_map(Location(0, -2)))

    def test_grid_doesnt_expand(self):
        world_map.TARGET_NUM_CELLS_PER_AVATAR = 4
        map = WorldMap(self._generate_grid())
        map.reconstruct_interactive_state(1)
        self.assertGridSize(map, 2)

    def test_scores_removed(self):
        world_map.SCORE_DESPAWN_CHANCE = 1
        grid = self._generate_grid()
        grid[Location(0, 1)].generates_score = True
        map = WorldMap(grid)
        map.reconstruct_interactive_state(1)
        self.assertEqual(len(list(map.score_cells())), 0)

    def test_score_despawn_chance(self):
        world_map.TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 0
        grid = self._generate_grid()
        grid[Location(0, 1)].generates_score = True
        map = WorldMap(grid)
        map.reconstruct_interactive_state(1)
        self.assertIn(grid[Location(0, 1)], map.score_cells())
        self.assertEqual(len(list(map.score_cells())), 1)

    def test_scores_added(self):
        world_map.TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 1
        map = WorldMap(self._generate_grid())
        map.reconstruct_interactive_state(1)
        self.assertEqual(len(list(map.score_cells())), 1)

        map.reconstruct_interactive_state(2)
        self.assertEqual(len(list(map.score_cells())), 2)

    def test_scores_not_added_when_at_target(self):
        world_map.TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 1
        grid = self._generate_grid()
        grid[Location(0, 1)].generates_score = True
        map = WorldMap(grid)
        map.reconstruct_interactive_state(1)
        self.assertEqual(len(list(map.score_cells())), 1)
        self.assertIn(grid[Location(0, 1)], map.score_cells())

    def test_no_score_cells_generated_if_no_suitable_cells(self):
        world_map.TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 1
        grid = self._generate_grid(1, 1)
        grid[Location(0, 0)].avatar = 'avatar'
        map = WorldMap(grid)
        map.reconstruct_interactive_state(1)
        self.assertEqual(len(list(map.score_cells())), 0)

    def test_pickups_added(self):
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 1
        world_map.PICKUP_SPAWN_CHANCE = 1
        map = WorldMap(self._generate_grid())
        map.reconstruct_interactive_state(1)
        self.assertEqual(len(list(map.pickup_cells())), 1)

        map.reconstruct_interactive_state(2)
        self.assertEqual(len(list(map.pickup_cells())), 2)

    def test_pickup_spawn_chance(self):
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 5
        world_map.PICKUP_SPAWN_CHANCE = 0
        grid = self._generate_grid()
        map = WorldMap(grid)
        map.reconstruct_interactive_state(1)
        self.assertEqual(len(list(map.pickup_cells())), 0)

    def test_pickups_not_added_when_at_target(self):
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 1
        grid = self._generate_grid()
        grid[Location(0, 1)].pickup = True
        map = WorldMap(grid)
        map.reconstruct_interactive_state(1)
        self.assertEqual(len(list(map.pickup_cells())), 1)
        self.assertIn(grid[Location(0, 1)], map.pickup_cells())

    def test_not_enough_pickup_space(self):
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 1
        grid = self._generate_grid(1, 1)
        grid[Location(0, 0)].generates_score = True
        map = WorldMap(grid)
        map.reconstruct_interactive_state(1)
        self.assertEqual(len(list(map.pickup_cells())), 0)

    def test_random_spawn_location(self):
        cell = MockCell()
        map = WorldMap({Location(0, 0): cell})
        self.assertEqual(map.get_random_spawn_location(), cell.location)

    def test_random_spawn_location_with_no_candidates(self):
        grid = self._generate_grid(1, 1)
        map = WorldMap(grid)
        grid[Location(0, 0)].avatar = True
        with self.assertRaises(IndexError):
            map.get_random_spawn_location()

    def test_can_move_to(self):
        map = WorldMap(self._generate_grid())
        target = Location(1, 1)
        self.assertTrue(map.can_move_to(target))

    def test_cannot_move_to_cell_off_grid(self):
        map = WorldMap(self._generate_grid())
        target = Location(4, 1)
        self.assertFalse(map.can_move_to(target))

    def test_cannot_move_to_uninhabitable_cell(self):
        target = Location(0, 0)
        cell = MockCell(target, habitable=False)
        map = WorldMap({target: cell})
        self.assertFalse(map.can_move_to(target))

    def test_cannot_move_to_habited_cell(self):
        target = Location(0, 0)
        cell = MockCell(target, avatar=DummyAvatar(target, 0))
        map = WorldMap({target: cell})
        target = Location(0, 0)
        self.assertFalse(map.can_move_to(target))

    def test_empty_list_grid(self):
        map = WorldMap([])
        self.assertFalse(map.is_on_map(Location(0, 0)))

    def test_empty_dict_grid(self):
        map = WorldMap({})
        self.assertFalse(map.is_on_map(Location(0, 0)))

    def test_iter(self):
        grid = [[MockCell(Location(-1, -1), name='A'), MockCell(Location(-1, 0), name='B'), MockCell(Location(-1, 1), name='C')],
                [MockCell(Location(0, -1), name='D'), MockCell(Location(0, 0), name='E'), MockCell(Location(0, 1), name='F')],
                [MockCell(Location(1, -1), name='E'), MockCell(Location(1, 0), name='G'), MockCell(Location(1, 1), name='H')],]
        map = WorldMap(self._grid_from_list(grid))
        self.assertEqual([list(column) for column in map], grid)


class TestWorldMapWithOriginCentre(TestWorldMap):
    def setUp(self):
        world_map.TARGET_NUM_CELLS_PER_AVATAR = 0
        world_map.TARGET_NUM_PICKUPS_PER_AVATAR = 0
        world_map.TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR = 0
        world_map.SCORE_DESPAWN_CHANCE = 0
        world_map.PICKUP_SPAWN_CHANCE = 0

    def _generate_grid(self, columns=2, rows=2):
        alphabet = iter(ascii_uppercase)
        grid = {Location(x, y): MockCell(Location(x, y), name=next(alphabet))
                for x in xrange(-columns/2+1, columns/2+1) for y in xrange(-rows/2+1, rows/2+1)}
        return grid

    def _generate_list_grid(self, columns=2, rows=2):
        alphabet = iter(ascii_uppercase)
        grid = []
        for x in xrange(-columns/2+1, columns/2+1):
            column = []
            for y in xrange(-rows/2+1, rows/2+1):
                column.append(MockCell(Location(x, y), name=next(alphabet)))
            grid.append(column)
        return grid

    def _grid_from_list(self, in_list):
        out = {}
        min_x = -len(in_list)/2 + 1
        min_y = -len(in_list[0])/2 + 1
        for i, column in enumerate(in_list):
            x = i + min_x
            for j, cell in enumerate(column):
                y = j + min_y
                out[Location(x, y)] = cell
        return out

    def test_retrieve_negative(self):
        map = WorldMap(self._generate_grid(3, 3))
        self.assertTrue(map.is_on_map(Location(-1, -1)))

    def test_retrieve_negative_from_list(self):
        map = WorldMap(self._generate_list_grid(2, 3))
        self.assertTrue(map.is_on_map(Location(0, -1)))
