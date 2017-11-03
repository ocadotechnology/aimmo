from unittest import TestCase

from mock_world import MockWorld

from simulation.location import Location
from simulation.pickups import HealthPickup


class TestHealthPickupAndEffects(TestCase):
    def test_health_pickups_and_effects_apply_default(self):
        game = MockWorld()
        game.game_state.add_avatar(1, None, Location(0, 0))
        cell = game.game_state.world_map.get_cell(Location(0, 0))
        self.assertEqual(cell.avatar, game.avatar_manager.get_avatar(1))
        self.assertEqual(cell.avatar.health, 5)

        cell = game.game_state.world_map.get_cell(Location(1, 0))
        cell.pickup = HealthPickup(cell)

        game.turn_manager._run_single_turn()

        self.assertEqual(cell.avatar, game.avatar_manager.get_avatar(1))
        self.assertEqual(cell.avatar.health, 8)

    def test_health_pickups_and_effects_apply_custom(self):
        game = MockWorld()
        game.game_state.add_avatar(1, None, Location(0, 0))
        cell = game.game_state.world_map.get_cell(Location(0, 0))
        self.assertEqual(cell.avatar, game.avatar_manager.get_avatar(1))
        self.assertEqual(cell.avatar.health, 5)

        cell = game.game_state.world_map.get_cell(Location(1, 0))
        cell.pickup = HealthPickup(cell, 10.5)

        game.turn_manager._run_single_turn()

        self.assertEqual(cell.avatar, game.avatar_manager.get_avatar(1))
        self.assertEqual(cell.avatar.health, 16)

    def test_health_effect_is_capped_at_100(self):
        game = MockWorld()
        game.game_state.add_avatar(1, None, Location(0, 0))
        cell = game.game_state.world_map.get_cell(Location(0, 0))
        self.assertEqual(cell.avatar, game.avatar_manager.get_avatar(1))
        self.assertEqual(cell.avatar.health, 5)

        cell = game.game_state.world_map.get_cell(Location(1, 0))
        cell.pickup = HealthPickup(cell, 100)

        game.turn_manager._run_single_turn()

        self.assertEqual(cell.avatar, game.avatar_manager.get_avatar(1))
        self.assertEqual(cell.avatar.health, 100)
