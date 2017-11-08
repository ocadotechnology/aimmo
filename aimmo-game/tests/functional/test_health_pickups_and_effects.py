import random
from unittest import TestCase

from hypothesis import given
import hypothesis.strategies as st

from mock_world import MockWorld

from simulation.location import Location
from simulation.pickups import HealthPickup, AVATAR_HEALTH_MAX, HEALTH_RESTORE_DEFAULT


class TestHealthPickupAndEffects(TestCase):
    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        self.game = MockWorld()
        self.game.game_state.add_avatar(1, None, Location(0, 0))
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))
        self.initial_health = self.game.avatar_manager.get_avatar(1).health

    def test_health_pickups_and_effects_apply_default(self):
        """
        HealthPickups without any parameter provided.
        """
        self.cell.pickup = HealthPickup(self.cell)

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.health, self.initial_health + HEALTH_RESTORE_DEFAULT)

    @given(st.integers(1, 100))
    def test_health_pickups_and_effects_apply_custom_integers(self, restore_value):
        """
        HealthPickups with explicit integer parameter provided.
        """
        self.setUp()
        self.cell.pickup = HealthPickup(self.cell, restore_value)

        self.game.turn_manager._run_single_turn()
        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))

        if self.initial_health + restore_value > 100:
            expected_result_health = 100
        else:
            expected_result_health = self.initial_health + restore_value

        self.assertEqual(self.cell.avatar.health, expected_result_health)

    @given(st.floats(1, 100))
    def test_health_pickups_and_effects_apply_custom_floats(self, restore_value):
        """
        HealthPickups with explicit float parameter provided.
        """
        self.setUp()
        self.cell.pickup = HealthPickup(self.cell, restore_value)

        self.game.turn_manager._run_single_turn()
        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))

        if self.initial_health + restore_value > 100:
            expected_result_health = 100
        else:
            expected_result_health = self.initial_health + int(round(restore_value))

        self.assertEqual(self.cell.avatar.health, expected_result_health)

    @given(st.integers(96, 100))
    def test_health_effect_is_capped_at_100(self, restore_value):
        """
        Make sure health cannot go above the maximum cap. Avatar health begins at 5hp,
        so every pickup in the 96-100 range would cause it to go above 100.
        """
        self.setUp()
        self.cell.pickup = HealthPickup(self.cell, restore_value)

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.health, AVATAR_HEALTH_MAX)
