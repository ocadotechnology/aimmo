from unittest import TestCase

from mock_world import MockWorld

from simulation.location import Location
from simulation.pickups import DamageBoostPickup


class TestDamagePickupsAndEffects(TestCase):
    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        self.game = MockWorld()
        self.game.game_state.add_avatar(1, None, Location(0, 0))
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))

    def test_damage_boost_pickup_can_be_picked_up_default(self):
        pickup_created = DamageBoostPickup(self.cell)
        self.cell.pickup = pickup_created

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(len(self.game.avatar_manager.get_avatar(1).effects), 1)
        damage_boost_effect = self.game.avatar_manager.get_avatar(1).effects.pop()
        self.assertTrue(isinstance(damage_boost_effect, pickup_created.EFFECT))

    def test_damage_boost_pickup_can_be_picked_up_custom(self):
        pickup_created = DamageBoostPickup(self.cell, 15)
        self.cell.pickup = pickup_created

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(len(self.game.avatar_manager.get_avatar(1).effects), 1)
        damage_boost_effect = self.game.avatar_manager.get_avatar(1).effects.pop()
        self.assertTrue(isinstance(damage_boost_effect, pickup_created.EFFECT))

    def test_damage_boost_pickup_effect_increases_avatar_strength_default(self):
        pickup_created = DamageBoostPickup(self.cell)
        self.cell.pickup = pickup_created

        self.game.turn_manager._run_single_turn()

        self.assertTrue(self.cell.avatar.attack_strength, 6)

    def test_damage_boost_pickup_effect_increases_avatar_strength_custom(self):
        pickup_created = DamageBoostPickup(self.cell, 10.5)
        self.cell.pickup = pickup_created

        self.game.turn_manager._run_single_turn()

        self.assertTrue(self.cell.avatar.attack_strength, 12)
