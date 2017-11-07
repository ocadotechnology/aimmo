from unittest import TestCase

from mock_world import MockWorld

from simulation.location import Location
from simulation.pickups import HealthPickup, HEALTH_RESTORE_DEFAULT, HEALTH_RESTORE_MAX, \
                               AVATAR_HEALTH_MAX


class TestHealthPickupAndEffects(TestCase):
    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        self.game = MockWorld()
        self.game.game_state.add_avatar(1, None, Location(0, 0))
        _avatar_spawn_cell = self.game.game_state.world_map.get_cell(Location(0, 0))
        self.initial_attack_strength = _avatar_spawn_cell.avatar.attack_strength
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))

    def test_health_pickups_and_effects_apply_default(self):
        self.cell.pickup = HealthPickup(self.cell)

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.health, 5 + HEALTH_RESTORE_DEFAULT)

    def test_health_pickups_and_effects_apply_custom(self):
        custom_value = 10.5
        self.assertNotEqual(int(round(custom_value)), HEALTH_RESTORE_DEFAULT)
        self.cell.pickup = HealthPickup(self.cell, custom_value)

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.health, 16)

    def test_health_effect_is_capped_at_100(self):
        self.cell.pickup = HealthPickup(self.cell, HEALTH_RESTORE_MAX)

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.health, AVATAR_HEALTH_MAX)
