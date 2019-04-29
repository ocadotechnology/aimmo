import asyncio
import random
from unittest import TestCase

import hypothesis.strategies as st
from hypothesis import given
from simulation.location import Location
from simulation.interactables.pickups import HealthPickup
from simulation.interactables.effects import (
    AVATAR_HEALTH_MAX,
    HEALTH_RESTORE_DEFAULT,
    HEALTH_RESTORE_MAX,
)

from .mock_world import MockWorld


class TestHealthPickupAndEffects(TestCase):
    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        self.game = MockWorld()
        self.game.simulation_runner.add_avatar(1, Location(0, 0))
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))
        self.initial_health = self.game.avatar_manager.get_avatar(1).health
        self.loop = asyncio.get_event_loop()

    def test_health_pickups_and_effects_apply_default(self):
        """
        HealthPickups without any parameter provided.
        """
        self.cell.interactable = HealthPickup(self.cell)
        self.assertEqual(
            self.cell.interactable.serialize(),
            {
                "type": "health",
                "location": {"x": self.cell.location.x, "y": self.cell.location.y},
            },
        )

        self.loop.run_until_complete(
            self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )
        )

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(
            self.cell.avatar.health, self.initial_health + HEALTH_RESTORE_DEFAULT
        )

    def test_health_effect_is_capped_at_HEALTH_RESTORE_MAX(self):
        """
        Make sure health cannot go above the maximum cap. Avatar health begins at 5hp,
        so every pickup in the 96-HEALTH_RESTORE_MAX range would cause it to go above
        HEALTH_RESTORE_MAX, until the initial health changes.
        """
        self.setUp()
        avatar = self.game.avatar_manager.get_avatar(1)
        avatar.health = 97
        self.cell.interactable = HealthPickup(self.cell)

        self.loop.run_until_complete(
            self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )
        )

        self.assertEqual(self.cell.avatar, self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.health, AVATAR_HEALTH_MAX)
