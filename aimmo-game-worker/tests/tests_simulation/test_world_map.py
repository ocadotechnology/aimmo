from __future__ import absolute_import

from unittest import TestCase

from simulation.location import Location
from simulation.world_map import WorldMap


class TestWorldMap(TestCase):
    AVATAR = {'location': {'x': 0, 'y': 0}, 'health': True, 'score': 3, 'events': []}

    def _generate_cells(self, columns=3, rows=3):
        cells = [{
            'location': {'x': x, 'y': y},
            'habitable': True,
            'generates_score': False,
            'avatar': None,
            'pickup': None,
        } for x in xrange(-columns / 2 + 1, 1 + columns / 2) for y in xrange(-rows / 2 + 1, 1 + rows / 2)]
        return cells

    def assertGridSize(self, map, expected_rows, expected_columns=None):
        if expected_columns is None:
            expected_columns = expected_rows
        self.assertEqual(len(list(map.all_cells())), expected_rows*expected_columns)

    def assertLocationsEqual(self, actual_cells, expected_locations):
        actual_cells = list(actual_cells)
        actual = frozenset(cell.location for cell in actual_cells)
        self.assertEqual(actual, frozenset(expected_locations))
        self.assertEqual(len(actual_cells), len(list(expected_locations)))

    def test_grid_size(self):
        map = WorldMap(self._generate_cells(1, 3))
        self.assertGridSize(map, 1, 3)

    def test_all_cells(self):
        map = WorldMap(self._generate_cells())
        self.assertLocationsEqual(map.all_cells(),
                                  [Location(x, y) for x in xrange(-1, 2) for y in xrange(-1, 2)])

    def test_score_cells(self):
        cells = self._generate_cells()
        cells[0]['generates_score'] = True
        cells[5]['generates_score'] = True
        map = WorldMap(cells)
        self.assertLocationsEqual(map.score_cells(), (Location(-1, -1), Location(0, 1)))

    def test_pickup_cells(self):
        cells = self._generate_cells()
        cells[0]['pickup'] = {'health_restored': 5}
        cells[8]['pickup'] = {'health_restored': 2}
        map = WorldMap(cells)
        self.assertLocationsEqual(map.pickup_cells(), (Location(-1, -1), Location(1, 1)))

    def test_location_is_visible(self):
        map = WorldMap(self._generate_cells())
        for x in (0, 1):
            for y in (0, 1):
                self.assertTrue(map.is_visible(Location(x, y)))

    def test_x_off_map_is_not_visible(self):
        map = WorldMap(self._generate_cells())
        for y in (0, 1):
            self.assertFalse(map.is_visible(Location(-2, y)))
            self.assertFalse(map.is_visible(Location(2, y)))

    def test_y_off_map_is_not_visible(self):
        map = WorldMap(self._generate_cells())
        for x in (0, 1):
            self.assertFalse(map.is_visible(Location(x, -2)))
            self.assertFalse(map.is_visible(Location(x, 2)))

    def test_get_valid_cell(self):
        map = WorldMap(self._generate_cells())
        for x in (0, 1):
            for y in (0, 1):
                location = Location(x, y)
                self.assertEqual(map.get_cell(location).location, location)

    def test_get_x_off_map(self):
        map = WorldMap(self._generate_cells())
        for y in (0, 1):
            with self.assertRaises(KeyError):
                map.get_cell(Location(-2, y))
            with self.assertRaises(KeyError):
                map.get_cell(Location(2, y))

    def test_get_y_off_map(self):
        map = WorldMap(self._generate_cells())
        for x in (0, 1):
            with self.assertRaises(KeyError):
                map.get_cell(Location(x, -2))
            with self.assertRaises(KeyError):
                map.get_cell(Location(x, 2))

    def test_can_move_to(self):
        map = WorldMap(self._generate_cells())
        target = Location(1, 1)
        self.assertTrue(map.can_move_to(target))

    def test_cannot_move_to_cell_off_grid(self):
        map = WorldMap(self._generate_cells())
        target = Location(4, 1)
        self.assertFalse(map.can_move_to(target))

    def test_cannot_move_to_uninhabitable_cell(self):
        cells = self._generate_cells()
        cells[0]['habitable'] = False
        map = WorldMap(cells)
        self.assertFalse(map.can_move_to(Location(-1, -1)))

    def test_cannot_move_to_habited_cell(self):
        cells = self._generate_cells()
        cells[1]['avatar'] = self.AVATAR
        map = WorldMap(cells)
        self.assertFalse(map.can_move_to(Location(-1, 0)))
