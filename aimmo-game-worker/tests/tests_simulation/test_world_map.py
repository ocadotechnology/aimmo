from __future__ import absolute_import

from unittest import TestCase

from simulation.location import Location
from simulation.world_map import WorldMap, WorldMapCreator


class TestWorldMap(TestCase):
    AVATAR = {
        "location": {"x": 0, "y": 0},
        "health": True,
        "score": 3,
        "backpack": [],
        "events": [],
    }

    def _generate_cells(self, columns=3, rows=3):
        cells = [
            {
                "location": {"x": x, "y": y},
                "habitable": True,
                "avatar": None,
                "interactable": None,
            }
            for x in range(-columns // 2 + 1, 1 + columns // 2)
            for y in range(-rows // 2 + 1, 1 + rows // 2)
        ]
        return cells

    def assertGridSize(self, map, expected_rows, expected_columns=None):
        if expected_columns is None:
            expected_columns = expected_rows
        self.assertEqual(len(list(map.all_cells())), expected_rows * expected_columns)

    def assertLocationsEqual(self, actual_cells, expected_locations):
        actual_cells = list(actual_cells)
        actual = frozenset(cell.location for cell in actual_cells)
        self.assertEqual(actual, frozenset(expected_locations))
        self.assertEqual(len(actual_cells), len(list(expected_locations)))

    def test_grid_size(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(
            self._generate_cells(1, 3)
        )
        self.assertGridSize(map, 1, 3)

    def test_all_cells(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        self.assertLocationsEqual(
            map.all_cells(),
            [Location(x, y) for x in range(-1, 2) for y in range(-1, 2)],
        )

    def test_score_cells(self):
        cells = self._generate_cells()
        cells[0]["interactable"] = {"type": "score"}
        cells[8]["interactable"] = {"type": "score"}
        map = WorldMapCreator.generate_world_map_from_cells_data(cells)
        self.assertLocationsEqual(map.score_cells(), (Location(-1, -1), Location(1, 1)))

    def test_interactable_cells(self):
        cells = self._generate_cells()
        cells[0]["interactable"] = {"type": "health"}
        cells[8]["interactable"] = {"type": "damage_boost"}
        map = WorldMapCreator.generate_world_map_from_cells_data(cells)
        self.assertLocationsEqual(
            map.interactable_cells(), (Location(-1, -1), Location(1, 1))
        )

    def test_artefact_cell(self):
        cells = self._generate_cells()
        cells[0]["interactable"] = {"type": "artefact"}
        map = WorldMapCreator.generate_world_map_from_cells_data(cells)
        self.assertEqual(map.get_cell(Location(-1, -1)).has_artefact(), True)

    def test_location_is_visible(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        for x in (0, 1):
            for y in (0, 1):
                self.assertTrue(map.is_visible(Location(x, y)))

    def test_x_off_map_is_not_visible(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        for y in (0, 1):
            self.assertFalse(map.is_visible(Location(-2, y)))
            self.assertFalse(map.is_visible(Location(2, y)))

    def test_y_off_map_is_not_visible(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        for x in (0, 1):
            self.assertFalse(map.is_visible(Location(x, -2)))
            self.assertFalse(map.is_visible(Location(x, 2)))

    def test_get_valid_cell(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        for x in (0, 1):
            for y in (0, 1):
                location = Location(x, y)
                self.assertEqual(map.get_cell(location).location, location)

    def test_get_x_off_map(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        for y in (0, 1):
            with self.assertRaises(KeyError):
                map.get_cell(Location(-2, y))
            with self.assertRaises(KeyError):
                map.get_cell(Location(2, y))

    def test_get_y_off_map(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        for x in (0, 1):
            with self.assertRaises(KeyError):
                map.get_cell(Location(x, -2))
            with self.assertRaises(KeyError):
                map.get_cell(Location(x, 2))

    def test_can_move_to(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        target = Location(1, 1)
        self.assertTrue(map.can_move_to(target))

    def test_cannot_move_to_cell_off_grid(self):
        map = WorldMapCreator.generate_world_map_from_cells_data(self._generate_cells())
        target = Location(4, 1)
        self.assertFalse(map.can_move_to(target))

    def test_cannot_move_to_uninhabitable_cell(self):
        cells = self._generate_cells()
        cells[0]["obstacle"] = {"location": {"x": -1, "y": -1}}
        map = WorldMapCreator.generate_world_map_from_cells_data(cells)
        self.assertFalse(map.can_move_to(Location(-1, -1)))

    def test_cannot_move_to_inhabited_cell(self):
        cells = self._generate_cells()
        cells[1]["avatar"] = self.AVATAR
        map = WorldMapCreator.generate_world_map_from_cells_data(cells)
        self.assertFalse(map.can_move_to(Location(-1, 0)))
