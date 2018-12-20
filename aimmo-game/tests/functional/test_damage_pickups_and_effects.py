from unittest import TestCase
from hypothesis import given, assume
from hypothesis import strategies as st
import math
import asyncio

from .mock_world import MockWorld
from simulation.location import Location
from simulation.pickups import DamageBoostPickup, DAMAGE_BOOST_DEFAULT


class TestDamagePickupsAndEffects(TestCase):
    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        self.game = MockWorld()
        self.game.game_state.add_avatar(1, Location(0, 0))
        _avatar_spawn_cell = self.game.game_state.world_map.get_cell(Location(0, 0))
        self.initial_attack_strength = _avatar_spawn_cell.avatar.attack_strength
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))
        self.loop = asyncio.get_event_loop()

    def test_damage_boost_pickup_can_be_picked_up_default(self):
        pickup_created = DamageBoostPickup(self.cell)
        self.cell.pickup = pickup_created

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(len(self.game.avatar_manager.get_avatar(1).effects), 1)
        damage_boost_effect = self.game.avatar_manager.get_avatar(1).effects.pop()
        self.assertTrue(isinstance(damage_boost_effect, pickup_created.EFFECT))

    @given(st.integers(min_value=1))
    def test_damage_boost_pickup_can_be_picked_up_custom_integer(self, boost_value):
        self.setUp()
        pickup_created = DamageBoostPickup(self.cell, boost_value)
        self.cell.pickup = pickup_created

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(len(self.game.avatar_manager.get_avatar(1).effects), 1)
        damage_boost_effect = self.game.avatar_manager.get_avatar(1).effects.pop()
        self.assertTrue(isinstance(damage_boost_effect, pickup_created.EFFECT))

    @given(st.floats(min_value=1))
    def test_damage_boost_pickup_can_be_picked_up_custom_floats(self, boost_value):
        assume(not math.isinf(boost_value))
        self.setUp()
        pickup_created = DamageBoostPickup(self.cell, boost_value)
        self.cell.pickup = pickup_created

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(len(self.game.avatar_manager.get_avatar(1).effects), 1)
        damage_boost_effect = self.game.avatar_manager.get_avatar(1).effects.pop()
        self.assertTrue(isinstance(damage_boost_effect, pickup_created.EFFECT))

    def test_damage_boost_increases_attack_strength_with_default_integer(self):
        """
        Damage boost with no value parameter provided (ie. default).
        """
        pickup_created = DamageBoostPickup(self.cell)
        self.cell.pickup = pickup_created

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertTrue(self.cell.avatar.attack_strength, self.initial_attack_strength + DAMAGE_BOOST_DEFAULT)

    @given(st.integers(min_value=1))
    def test_damage_boost_increases_attack_strength_with_custom_integers(self, boost_value):
        """
        Damage Boost with random integers provided as a parameter.
        """
        self.setUp()
        pickup_created = DamageBoostPickup(self.cell, boost_value)
        self.cell.pickup = pickup_created

        self.loop.run_until_complete(self.game.simulation_runner.run_single_turn(self.game.avatar_manager.get_player_id_to_serialised_action()))

        self.assertTrue(self.cell.avatar.attack_strength, self.initial_attack_strength + boost_value)
