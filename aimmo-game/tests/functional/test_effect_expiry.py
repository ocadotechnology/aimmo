from unittest import TestCase
import asyncio

from .mock_world import MockWorld

from simulation.location import Location
from simulation.pickups import DamageBoostPickup, InvulnerabilityPickup
from simulation.effects import INVULNERABILITY_RESISTANCE


class TestEffectExpiry(TestCase):
    """
    Tests if effects of pickups can expire correctly in multiple scenarios. Note: applies only to pickups that inherit
    TimedEffect!
    """

    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        SETTINGS = {
            'START_HEIGHT': 5,
            'START_WIDTH': 15,
            'OBSTACLE_RATIO': 0,
        }

        self.game = MockWorld(SETTINGS)
        self.game.game_state.add_avatar(1, Location(0, 0))
        self.avatar = self.game.avatar_manager.get_avatar(1)
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))

    def test_single_damage_boost_pickup_expiry(self):
        """
        Avatar spawns at ORIGIN. DamageBoostPickup is at 1,0. Avatar moves to the pickup and picks it up next turn and
        then we wait for the effect to expire EFFECT_TIME turns later (value defined in the effects class).
        """
        pickup_created = DamageBoostPickup(self.cell, 10)
        self.cell.pickup = pickup_created
        self.assertEqual(self.avatar.attack_strength, 1)

        # Avatar moves EAST to (1,0) where pickup is located, then repeats it 5 times.
        loop = asyncio.get_event_loop()
        for i in range(6):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        self.assertTrue(isinstance(list(self.avatar.effects)[0], pickup_created.EFFECT))
        self.assertEqual(list(self.avatar.effects)[0]._time_remaining, 5)
        self.assertEqual(self.avatar.attack_strength, 11)

        # Run 5 more turns and expect the effect to expire.
        for i in range(5):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        self.assertEqual(len(self.avatar.effects), 0)
        self.assertEqual(self.avatar.attack_strength, 1)

    def test_single_invulnerability_pickup_pickup_expiry(self):
        """
        Avatar spawns at ORIGIN. InvulnerabilityPickup is at 1,0. Avatar moves to the pickup and picks it up next turn
        and then we wait for the effect to expire EFFECT_TIME turns later (value defined in the effects class).
        """
        pickup_created = InvulnerabilityPickup(self.cell)
        self.cell.pickup = pickup_created
        self.assertEqual(self.avatar.resistance, 0)

        # Avatar moves EAST to (1,0) where pickup is located, then repeats it 5 times.
        loop = asyncio.get_event_loop()
        for i in range(6):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertTrue(isinstance(list(self.avatar.effects)[0], pickup_created.EFFECT))
        self.assertEqual(list(self.avatar.effects)[0]._time_remaining, 5)
        self.assertEqual(self.avatar.resistance, INVULNERABILITY_RESISTANCE)

        # Run 5 more turns and expect the effect to expire.
        for i in range(5):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertEqual(len(self.avatar.effects), 0)
        self.assertEqual(self.avatar.resistance, 0)

    def test_multiple_damage_boost_pickup_expiry(self):
        """
        Ensure that each damage boost effect expires at the appropriate time, even if the user stacks up on them. One
        pickup will be at (1,0) and another at (3,0).
        """
        cell_one = self.game.game_state.world_map.get_cell(Location(1, 0))
        cell_two = self.game.game_state.world_map.get_cell(Location(3, 0))
        pickup_created_one = DamageBoostPickup(cell_one, 10)
        pickup_created_two = DamageBoostPickup(cell_two, 15)

        cell_one.pickup = pickup_created_one
        cell_two.pickup = pickup_created_two

        self.assertEqual(self.avatar.attack_strength, 1)

        # Avatar moves EAST to (1,0) where pickup one is located.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.game.simulation_runner.run_single_turn(
            self.game.avatar_manager.get_player_id_to_serialised_action()
        ))

        self.assertTrue(isinstance(list(self.avatar.effects)[0], pickup_created_one.EFFECT))
        self.assertEqual(len(self.avatar.effects), 1)
        self.assertEqual(list(self.avatar.effects)[0]._time_remaining, 10)
        self.assertEqual(self.avatar.attack_strength, 11)

        # Move twice to the second pickup.
        for i in range(2):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        self.assertTrue(isinstance(list(self.avatar.effects)[1], pickup_created_two.EFFECT))
        self.assertEqual(len(self.avatar.effects), 2)
        self.assertEqual(self.avatar.attack_strength, 26)

        # Eight turns later, we expect the first effect to expire.
        for i in range(8):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        self.assertEqual(len(self.avatar.effects), 1)
        self.assertEqual(list(self.avatar.effects)[0]._time_remaining, 2)
        self.assertEqual(self.avatar.attack_strength, 16)

        # Two turns later, the second pickup expires too.
        for i in range(2):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        self.assertEqual(len(self.avatar.effects), 0)
        self.assertEqual(self.avatar.attack_strength, 1)

    def test_multiple_invulnerability_boost_pickup_expiry(self):
        """
        Ensure that each invulnerability boost effect expires at the appropriate time, even if the user stacks up on
        them. One pickup will be at (1,0) and another at (3,0).
        """
        cell_one = self.game.game_state.world_map.get_cell(Location(1, 0))
        cell_two = self.game.game_state.world_map.get_cell(Location(3, 0))
        pickup_created_one = InvulnerabilityPickup(cell_one)
        pickup_created_two = InvulnerabilityPickup(cell_two)

        cell_one.pickup = pickup_created_one
        cell_two.pickup = pickup_created_two

        self.assertEqual(self.avatar.resistance, 0)

        # Avatar moves EAST to (1,0) where pickup one is located.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.game.simulation_runner.run_single_turn(
            self.game.avatar_manager.get_player_id_to_serialised_action()
        ))

        self.assertTrue(isinstance(list(self.avatar.effects)[0], pickup_created_one.EFFECT))
        self.assertEqual(len(self.avatar.effects), 1)
        self.assertEqual(list(self.avatar.effects)[0]._time_remaining, 10)
        self.assertEqual(self.avatar.resistance, INVULNERABILITY_RESISTANCE)

        # Move twice to the second pickup.
        for i in range(2):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        self.assertTrue(isinstance(list(self.avatar.effects)[1], pickup_created_two.EFFECT))
        self.assertEqual(len(self.avatar.effects), 2)
        self.assertEqual(self.avatar.resistance, INVULNERABILITY_RESISTANCE * 2)

        # Eight turns later, we expect the first effect to expire.
        for i in range(8):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        self.assertEqual(len(self.avatar.effects), 1)
        self.assertEqual(list(self.avatar.effects)[0]._time_remaining, 2)
        self.assertEqual(self.avatar.resistance, INVULNERABILITY_RESISTANCE)

        # Two turns later, the second pickup expires too.
        for i in range(2):
            loop.run_until_complete(self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialised_action()
            ))

        self.assertEqual(len(self.avatar.effects), 0)
        self.assertEqual(self.avatar.resistance, 0)
