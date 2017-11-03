from unittest import TestCase

from mock_world import MockWorld

from simulation.location import Location
from simulation.pickups import DamageBoostPickup, DAMAGE_BOOST_DEFAULT


class TestDamagePickupsAndEffects(TestCase):
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

    def test_damage_boost_pickup_can_be_picked_up_default(self):
        pickup_created = DamageBoostPickup(self.cell)
        self.cell.pickup = pickup_created

        self.game.turn_manager._run_single_turn()

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(len(self.game.avatar_manager.get_avatar(1).effects), 1)
        damage_boost_effect = self.game.avatar_manager.get_avatar(1).effects.pop()
        self.assertTrue(isinstance(damage_boost_effect, pickup_created.EFFECT))

    def test_damage_boost_pickup_can_be_picked_up_custom(self):
        custom_value = 15
        self.assertNotEqual(custom_value, DAMAGE_BOOST_DEFAULT)
        pickup_created = DamageBoostPickup(self.cell, custom_value)
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

        self.assertTrue(self.cell.avatar.attack_strength, self.initial_attack_strength + DAMAGE_BOOST_DEFAULT)

    def test_damage_boost_pickup_effect_increases_avatar_strength_custom(self):
        pickup_created = DamageBoostPickup(self.cell, 10.5)
        self.cell.pickup = pickup_created

        self.game.turn_manager._run_single_turn()

        self.assertTrue(self.cell.avatar.attack_strength, self.initial_attack_strength + 11)
