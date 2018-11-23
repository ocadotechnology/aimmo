from unittest import TestCase
import asyncio

from .mock_world import MockWorld
from simulation.location import Location
from simulation import map_generator
from simulation.simulation_runner import ConcurrentSimulationRunner
from tests.test_simulation.dummy_avatar import (
    MoveEastDummy, MoveWestDummy, MoveNorthDummy, MoveSouthDummy, WaitDummy, DeadDummy
)


class TestMovementsInMap(TestCase):

    SETTINGS = {
        'START_HEIGHT': 50,
        'START_WIDTH': 50,
        'OBSTACLE_RATIO': 0,
    }

    def set_up_environment(self, dummy_list=None, location=Location(0, 0),
                           map_generator_class=map_generator.Main):
        """
        Utility method for testing.
        """
        self.game = MockWorld(TestMovementsInMap.SETTINGS, dummy_list,
                              map_generator_class, ConcurrentSimulationRunner)
        self.game.game_state.add_avatar(player_id=1, location=location)
        self.avatar = self.game.avatar_manager.get_avatar(1)

    def set_up_and_make_movements_in_a_single_direction(self, dummy_list,
                                                        number_of_movements,
                                                        spawn=Location(0, 0)):
        """
        Template function for repetitive movements in a single direction.
        """
        self.set_up_environment(dummy_list, spawn)
        self.assertEqual(self.avatar.location, spawn)

        loop = asyncio.get_event_loop()
        for i in range(number_of_movements):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

    def test_movement_five_times_in_all_directions(self):
        """
        Moves the avatar to the edge of the map. Each time it moves the avatar 5 times
        from origin in all cardinal directions.
        """

        # East.
        self.set_up_and_make_movements_in_a_single_direction([MoveEastDummy], 5)
        self.assertEqual(self.avatar.location, Location(5, 0))

        # West.
        self.set_up_and_make_movements_in_a_single_direction([MoveWestDummy], 5)
        self.assertEqual(self.avatar.location, Location(-5, 0))

        # North.
        self.set_up_and_make_movements_in_a_single_direction([MoveNorthDummy], 5)
        self.assertEqual(self.avatar.location, Location(0, 5))

        # South.
        self.set_up_and_make_movements_in_a_single_direction([MoveSouthDummy], 5)
        self.assertEqual(self.avatar.location, Location(0, -5))

    def test_move_towards_map_boundaries(self):
        """
        Tests game behaviour when the avatar tries to move towards one of the four of the
        maps boundaries.
        """

        # North boundary.
        self.set_up_and_make_movements_in_a_single_direction([MoveNorthDummy], 2,
                                                             Location(0, 25))

        self.assertFalse(self.game.game_state.world_map.is_on_map(Location(0, 26)))
        self.assertEqual(self.avatar.location, Location(0, 25))

        # South boundary.
        self.set_up_and_make_movements_in_a_single_direction([MoveSouthDummy], 2,
                                                             Location(0, -24))

        self.assertFalse(self.game.game_state.world_map.is_on_map(Location(0, -25)))
        self.assertEqual(self.avatar.location, Location(0, -24))

        # East boundary.
        self.set_up_and_make_movements_in_a_single_direction([MoveEastDummy], 2,
                                                             Location(25, 0))

        self.assertFalse(self.game.game_state.world_map.is_on_map(Location(26, 0)))
        self.assertEqual(self.avatar.location, Location(25, 0))

        # West boundary.
        self.set_up_and_make_movements_in_a_single_direction([MoveWestDummy], 2,
                                                             Location(-24, 0))

        self.assertFalse(self.game.game_state.world_map.is_on_map(Location(-25, 0)))
        self.assertEqual(self.avatar.location, Location(-24, 0))

    def test_avatar_cannot_move_into_obstacle(self):
        """
        Make sure that an avatar will stay in its location when trying to move into a
        obstacle cell.
        """
        self.set_up_environment([MoveEastDummy])
        obstacle_cell = self.game.game_state.world_map.get_cell(Location(2, 0))
        obstacle_cell.habitable = False
        self.assertTrue(self.avatar.location, Location(0, 0))

        loop = asyncio.get_event_loop()
        for i in range(2):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertTrue(self.avatar.location, Location(1, 0))

    def test_avatars_cannot_go_into_each_other(self):
        """
        Two avatars moving in the same direction towards each other.
        """
        # Even number of cells between two avatars.
        self.set_up_environment([MoveEastDummy, MoveWestDummy])
        self.game.game_state.add_avatar(2, Location(3, 0))
        avatar_two = self.game.avatar_manager.get_avatar(2)

        self.assertEqual(self.avatar.location, Location(0, 0))
        self.assertEqual(avatar_two.location, Location(3, 0))
        loop = asyncio.get_event_loop()
        for i in range(2):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        # Avatar 1 & Avatar 2 only managed to move once.
        self.assertEqual(self.avatar.location, Location(1, 0))
        self.assertEqual(avatar_two.location, Location(2, 0))

        # Odd number of cells between two avatars.
        self.set_up_environment([MoveEastDummy, MoveWestDummy])
        self.game.game_state.add_avatar(2, Location(4, 0))
        avatar_two = self.game.avatar_manager.get_avatar(2)

        self.assertEqual(self.avatar.location, Location(0, 0))
        self.assertEqual(avatar_two.location, Location(4, 0))

        for i in range(2):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        # Avatar 1 & Avatar 2 managed to only move only once.
        self.assertEqual(self.avatar.location, Location(1, 0))
        self.assertEqual(avatar_two.location, Location(3, 0))

        # Live avatar can't move into a square occupied by a 'dead' (no worker) avatar
        self.set_up_environment([DeadDummy, MoveWestDummy])
        self.game.game_state.add_avatar(2, Location(1, 0))
        avatar_two = self.game.avatar_manager.get_avatar(2)

        self.assertEqual(self.avatar.location, Location(0, 0))
        self.assertEqual(avatar_two.location, Location(1, 0))
        loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertEqual(self.avatar.location, Location(0, 0))
        self.assertEqual(avatar_two.location, Location(1, 0))

    def test_wait_action_on_a_single_avatar(self):
        """
        Ensures a returned WaitAction will keep the avatar in its initial location.
        """
        self.set_up_environment(dummy_list=[WaitDummy])
        self.assertEqual(self.avatar.location, Location(0, 0))

        loop = asyncio.get_event_loop()
        for i in range(5):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertEqual(self.avatar.location, Location(0, 0))
