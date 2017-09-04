from unittest import TestCase

from simulation.world_map import Cell
from simulation.location import Location
from simulation.direction import EAST, WEST, NORTH, SOUTH
from simulation.avatar.avatar_view import AvatarView


class MockWorldMap(object):
    def __init__(self, _min_x, _min_y, _max_x, _max_y):
        self._min_x = _min_x
        self._min_y = _min_y
        self._max_x = _max_x
        self._max_y = _max_y

    def min_x(self):
        return self._min_x

    def min_y(self):
        return self._min_y

    def max_x(self):
        return self._max_x

    def max_y(self):
        return self._max_y

    def get_cell(self, location):
        if not location is None:
            return Cell(location)
        else:
            raise ValueError


class TestAvatarView(TestCase):
    def setUp(self):
        pass

    # Test 'location_in_view'

    def test_knows_when_a_location_is_inside_the_view(self):
        avatar_view = AvatarView(Location(0, 0), 2)
        self.assertTrue(avatar_view.location_in_view(Location(0, 0)))
        self.assertTrue(avatar_view.location_in_view(Location(2, 2)))
        self.assertTrue(avatar_view.location_in_view(Location(2, -2)))
        self.assertTrue(avatar_view.location_in_view(Location(-2, 2)))
        self.assertTrue(avatar_view.location_in_view(Location(-2, -2)))

    def test_knows_when_a_location_is_outside_the_view(self):
        avatar_view = AvatarView(Location(1, 1), 1)
        self.assertFalse(avatar_view.location_in_view(Location(3, 0)))
        self.assertFalse(avatar_view.location_in_view(Location(0, 5)))
        self.assertFalse(avatar_view.location_in_view(Location(-4, -4)))

    # Test 'cells_in_rectangle'

    def test_returns_one_cell_when_world_map_is_empty(self):
        mock_world_map = MockWorldMap(0, 0, 0, 0)
        cells_in_rectangle = AvatarView.cells_in_rectangle(Location(-3, 4), Location(5, -6), mock_world_map)
        self.assertEqual(len(cells_in_rectangle), 1)

    def test_returns_no_cells_when_the_corners_are_wrong(self):
        mock_world_map = MockWorldMap(-1, -1, 1, 1)
        cells_in_rectangle = AvatarView.cells_in_rectangle(Location(1, -1), Location(-1, 1), mock_world_map)
        self.assertEqual(len(cells_in_rectangle), 0)

    def test_returns_no_cells_when_the_rectangle_is_misplaced(self):
        mock_world_map = MockWorldMap(-2, -1, 6, 1)
        cells_in_rectangle = AvatarView.cells_in_rectangle(Location(-5, 0), Location(-2, -1), mock_world_map)
        self.assertEqual(len(cells_in_rectangle), 0)

    def test_returns_correct_number_of_cells_when_the_rectangle_is_fully_inside_the_map(self):
        mock_world_map = MockWorldMap(-6, -8, 10, 9)
        cells_in_rectangle = AvatarView.cells_in_rectangle(Location(-2, 1), Location(2, -1), mock_world_map)
        self.assertEqual(len(cells_in_rectangle), 8)

    def test_returns_correct_number_of_cells_when_the_rectangle_is_partially_inisde_the_map(self):
        mock_world_map = MockWorldMap(0, 0, 5, 5)
        cells_in_rectagle = AvatarView.cells_in_rectangle(Location(-1, 1), Location(1, -1), mock_world_map)
        self.assertEqual(len(cells_in_rectagle), 1)

    # Test 'reveal_all_cells'

    def test_reveals_all_cells(self):
        mock_world_map = MockWorldMap(-25, -30, 30, 40)
        avatar_view = AvatarView(Location(-4, -8), 2)
        avatar_view.reveal_all_cells(mock_world_map)
        self.assertEqual(len(avatar_view.cells_to_reveal), 16)

    # Test 'move'

    def test_correct_number_of_cells_to_clear_reveal_and_in_view(self):
        mock_world_map = MockWorldMap(-10, -10, 10, 10)
        avatar_view = AvatarView(Location(0, 0), 2)
        avatar_view.reveal_all_cells(mock_world_map)
        self.assertEqual(len(avatar_view.cells_to_reveal), 16)
        self.assertEqual(len(avatar_view.cells_in_view), 16)
        avatar_view.move(EAST, mock_world_map)
        self.assertEqual(len(avatar_view.cells_to_reveal), 4)
        self.assertEqual(len(avatar_view.cells_to_clear), 24)
        self.assertEqual(len(avatar_view.cells_in_view), 16)

    def test_horizons_are_updated_accordingly(self):
        mock_world_map = MockWorldMap(0, -12, 9, 2)
        avatar_view = AvatarView(Location(4, -5), 1)
        initial_NW_horizon = avatar_view.NW_horizon
        initial_NE_horizon = avatar_view.NE_horizon
        initial_SW_horizon = avatar_view.SW_horizon
        initial_SE_horizon = avatar_view.SE_horizon
        avatar_view.move(SOUTH, mock_world_map)
        self.assertEqual(avatar_view.NW_horizon, initial_NW_horizon + SOUTH)
        self.assertEqual(avatar_view.NE_horizon, initial_NE_horizon + SOUTH)
        self.assertEqual(avatar_view.SW_horizon, initial_SW_horizon + SOUTH)
        self.assertEqual(avatar_view.SE_horizon, initial_SE_horizon + SOUTH)

    def test_chain_of_moves(self):
        mock_world_map = MockWorldMap(-26, -32, 22, 27)
        avatar_view = AvatarView(Location(1, 1), 3)
        avatar_view.reveal_all_cells(mock_world_map)
        initial_cells_in_view = set(avatar_view.cells_in_view)
        avatar_view.move(EAST, mock_world_map)
        avatar_view.move(SOUTH, mock_world_map)
        avatar_view.move(WEST, mock_world_map)
        avatar_view.move(NORTH, mock_world_map)
        self.assertEqual(avatar_view.cells_in_view, initial_cells_in_view)