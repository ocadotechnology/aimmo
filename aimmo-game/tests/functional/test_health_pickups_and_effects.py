import random
from unittest import TestCase
import asyncio

from hypothesis import given
import hypothesis.strategies as st

from .mock_world import MockWorld

from simulation.location import Location
from simulation.pickups import (
    HealthPickup, AVATAR_HEALTH_MAX, HEALTH_RESTORE_DEFAULT, HEALTH_RESTORE_MAX
)


class TestHealthPickupAndEffects(TestCase):
    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        self.game = MockWorld()
        self.game.game_state.add_avatar(1, Location(0, 0))
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))
        self.initial_health = self.game.avatar_manager.get_avatar(1).health
        self.loop = asyncio.get_event_loop()

    def test_health_pickups_and_effects_apply_default(self):
        """
        HealthPickups without any parameter provided.
        """
        self.cell.pickup = HealthPickup(self.cell)

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.health, self.initial_health +
                         HEALTH_RESTORE_DEFAULT)

    @given(st.integers(1, HEALTH_RESTORE_MAX))
    def test_health_pickups_and_effects_apply_custom_integers(self, restore_value):
        """
        HealthPickups with explicit integer parameter provided.
        """
        self.setUp()
        self.cell.pickup = HealthPickup(self.cell, restore_value)

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))
        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))

        if self.initial_health + restore_value > HEALTH_RESTORE_MAX:
            expected_result_health = HEALTH_RESTORE_MAX
        else:
            expected_result_health = self.initial_health + restore_value

        self.assertEqual(self.cell.avatar.health, expected_result_health)

    @given(st.floats(1, HEALTH_RESTORE_MAX))
    def test_health_pickups_and_effects_apply_custom_floats(self, restore_value):
        """
        HealthPickups with explicit float parameter provided.
        """
        self.setUp()
        self.cell.pickup = HealthPickup(self.cell, restore_value)

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))
        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))

        if self.initial_health + restore_value > HEALTH_RESTORE_MAX:
            expected_result_health = HEALTH_RESTORE_MAX
        else:
            expected_result_health = self.initial_health + int(round(restore_value))

        self.assertEqual(self.cell.avatar.health, expected_result_health)

    @given(st.integers(96, HEALTH_RESTORE_MAX))
    def test_health_effect_is_capped_at_HEALTH_RESTORE_MAX(self, restore_value):
        """
        Make sure health cannot go above the maximum cap. Avatar health begins at 5hp,
        so every pickup in the 96-HEALTH_RESTORE_MAX range would cause it to go above
        HEALTH_RESTORE_MAX, until the initial health changes.
        """
        self.setUp()
        self.cell.pickup = HealthPickup(self.cell, restore_value)

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.health, AVATAR_HEALTH_MAX)
