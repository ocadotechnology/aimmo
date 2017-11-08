from unittest import TestCase

from mock_world import MockWorld
from simulation.location import Location
from tests.test_simulation.dummy_avatar import MoveEastDummy, MoveWestDummy, MoveNorthDummy, MoveSouthDummy


class TestMapMovements(TestCase):

    SETTINGS = {
        'START_HEIGHT': 50,
        'START_WIDTH': 50,
        'OBSTACLE_RATIO': 0,
    }

    def set_up_environment(self, dummy_list=None, location=Location(0,0)):
        self.game = MockWorld(TestMapMovements.SETTINGS, dummy_list)
        self.game.game_state.add_avatar(1, None, location)
        self.avatar = self.game.avatar_manager.get_avatar(1)

    def test_movement_five_times_in_all_directions(self):
        """
        Consists of four tests. Each one moves the avatar 5 times from origin in all cardinal directions.
        """

        # East.
        self.set_up_environment([MoveEastDummy])
        self.assertEqual(self.avatar.location, Location(0, 0))

        for i in range(5):
            self.game.turn_manager._run_single_turn()

        self.assertEqual(self.avatar.location, Location(5, 0))

        # West.
        self.set_up_environment([MoveWestDummy])
        self.assertEqual(self.avatar.location, Location(0, 0))

        for i in range(5):
            self.game.turn_manager._run_single_turn()

        self.assertEqual(self.avatar.location, Location(-5, 0))

        # North.
        self.set_up_environment([MoveNorthDummy])
        self.assertEqual(self.avatar.location, Location(0, 0))

        for i in range(5):
            self.game.turn_manager._run_single_turn()

        self.assertEqual(self.avatar.location, Location(0, 5))

        # South.
        self.set_up_environment([MoveSouthDummy])
        self.assertEqual(self.avatar.location, Location(0, 0))

        for i in range(5):
            self.game.turn_manager._run_single_turn()

        self.assertEqual(self.avatar.location, Location(0, -5))

    def test_move_towards_map_boundaries(self):
        """
        Tests game behaviour when the avatar tries to move towards one of the four of the maps boundaries.
        """

        # North boundary.
        self.set_up_environment([MoveNorthDummy], Location(0, 25))
        self.assertFalse(self.game.game_state.world_map.is_on_map(Location(0, 26)))

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.avatar.location, Location(0, 25))

        # South boundary.
        self.set_up_environment([MoveSouthDummy], Location(0, -24))
        self.assertFalse(self.game.game_state.world_map.is_on_map(Location(0, -25)))

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.avatar.location, Location(0, -24))

        # East boundary.
        self.set_up_environment([MoveEastDummy], Location(25, 0))
        self.assertFalse(self.game.game_state.world_map.is_on_map(Location(26, 0)))

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.avatar.location, Location(25, 0))

        # West boundary.
        self.set_up_environment([MoveWestDummy], Location(-24, 0))
        self.assertFalse(self.game.game_state.world_map.is_on_map(Location(-25, 0)))

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.avatar.location, Location(-24, 0))
