import asyncio
import math
from unittest import TestCase

from hypothesis import assume, given
from hypothesis import strategies as st
from simulation.location import Location
from simulation.interactables.pickups import DamageBoostPickup
from simulation.interactables.effects import DAMAGE_BOOST_DEFAULT

from .mock_world import MockWorld


class TestDamagePickupsAndEffects(TestCase):
    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        self.game = MockWorld()
        self.game.simulation_runner.add_avatar(1, Location(0, 0))
        _avatar_spawn_cell = self.game.game_state.world_map.get_cell(Location(0, 0))
        self.initial_attack_strength = _avatar_spawn_cell.avatar.attack_strength
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))
        self.loop = asyncio.get_event_loop()

    def test_damage_boost_pickup_can_be_picked_up_default(self):
        pickup_created = DamageBoostPickup(self.cell)
        self.cell.interactable = pickup_created
        self.assertEqual(
            self.cell.interactable.serialize(),
            {
                "type": "damage_boost",
                "location": {"x": self.cell.location.x, "y": self.cell.location.y},
            },
        )
        self.loop.run_until_complete(
            self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )
        )

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(len(self.game.avatar_manager.get_avatar(1).effects), 1)
        damage_boost_effect = self.game.avatar_manager.get_avatar(1).effects.pop()
        self.assertTrue(isinstance(damage_boost_effect, pickup_created.effects[0]))

    def test_damage_boost_increases_attack_strength_with_default_integer(self):
        """
        Damage boost with no value parameter provided (ie. default).
        """
        pickup_created = DamageBoostPickup(self.cell)
        self.cell.interactable = pickup_created

        self.loop.run_until_complete(
            self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )
        )

        self.assertTrue(
            self.cell.avatar.attack_strength,
            self.initial_attack_strength + DAMAGE_BOOST_DEFAULT,
        )
