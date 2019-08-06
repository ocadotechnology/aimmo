import pytest
import asyncio

from simulation.location import Location
from simulation.interactables.pickups import DamageBoostPickup, InvulnerabilityPickup
from simulation.interactables.effects import (
    DAMAGE_BOOST_DEFAULT,
    INVULNERABILITY_RESISTANCE,
)

from .mock_world import MockWorld


class TestEffectExpiry:
    """
    Tests if effects of pickups can expire correctly in multiple scenarios. Note: applies only to pickups that inherit
    TimedEffect!
    """

    def setup_method(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        SETTINGS = {"START_HEIGHT": 5, "START_WIDTH": 15, "OBSTACLE_RATIO": 0}

        self.game = MockWorld(SETTINGS)
        self.game.simulation_runner.add_avatar(1, Location(0, 0))
        self.avatar = self.game.avatar_manager.get_avatar(1)
        self.cell = self.game.game_state.world_map.get_cell(Location(1, 0))

    async def test_single_damage_boost_pickup_expiry(self, loop):
        """
        Avatar spawns at ORIGIN. DamageBoostPickup is at 1,0. Avatar moves to the pickup and picks it up next turn and
        then we wait for the effect to expire EFFECT_TIME turns later (value defined in the effects class).
        """
        pickup_created = DamageBoostPickup(self.cell)
        self.cell.interactable = pickup_created
        assert self.avatar.attack_strength == 1

        # Avatar moves EAST to (1,0) where pickup is located, then repeats it 5 times.
        for i in range(6):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert isinstance(list(self.avatar.effects)[0], pickup_created.effects[0])
        assert list(self.avatar.effects)[0]._time_remaining == 5
        assert self.avatar.attack_strength == DAMAGE_BOOST_DEFAULT + 1

        # Run 5 more turns and expect the effect to expire.
        for i in range(5):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert len(self.avatar.effects) == 0
        assert self.avatar.attack_strength == 1

    async def test_single_invulnerability_pickup_pickup_expiry(self, loop):
        """
        Avatar spawns at ORIGIN. InvulnerabilityPickup is at 1,0. Avatar moves to the pickup and picks it up next turn
        and then we wait for the effect to expire EFFECT_TIME turns later (value defined in the effects class).
        """
        pickup_created = InvulnerabilityPickup(self.cell)
        self.cell.interactable = pickup_created
        assert self.avatar.resistance == 0

        # Avatar moves EAST to (1,0) where pickup is located, then repeats it 5 times.
        for i in range(6):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert isinstance(list(self.avatar.effects)[0], pickup_created.effects[0])
        assert list(self.avatar.effects)[0]._time_remaining == 5
        assert self.avatar.resistance == INVULNERABILITY_RESISTANCE

        # Run 5 more turns and expect the effect to expire.
        for i in range(5):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert len(self.avatar.effects) == 0
        assert self.avatar.resistance == 0

    async def test_multiple_damage_boost_pickup_expiry(self, loop):
        """
        Ensure that each damage boost effect expires at the appropriate time, even if the user stacks up on them. One
        pickup will be at (1,0) and another at (3,0).
        """
        cell_one = self.game.game_state.world_map.get_cell(Location(1, 0))
        cell_two = self.game.game_state.world_map.get_cell(Location(3, 0))
        pickup_created_one = DamageBoostPickup(cell_one)
        pickup_created_two = DamageBoostPickup(cell_two)

        cell_one.interactable = pickup_created_one
        cell_two.interactable = pickup_created_two

        assert self.avatar.attack_strength == 1

        # Avatar moves EAST to (1,0) where pickup one is located.
        await self.game.simulation_runner.run_single_turn(
            self.game.avatar_manager.get_player_id_to_serialized_action()
        )

        assert isinstance(list(self.avatar.effects)[0], pickup_created_one.effects[0])
        assert len(self.avatar.effects) == 1
        assert list(self.avatar.effects)[0]._time_remaining == 10
        assert self.avatar.attack_strength == DAMAGE_BOOST_DEFAULT + 1

        # Move twice to the second pickup.
        for i in range(2):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert isinstance(list(self.avatar.effects)[1], pickup_created_two.effects[0])
        assert len(self.avatar.effects) == 2
        assert self.avatar.attack_strength == DAMAGE_BOOST_DEFAULT * 2 + 1

        # Eight turns later, we expect the first effect to expire.
        for i in range(8):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert len(self.avatar.effects) == 1
        assert list(self.avatar.effects)[0]._time_remaining == 2
        assert self.avatar.attack_strength == DAMAGE_BOOST_DEFAULT + 1

        # Two turns later, the second pickup expires too.
        for i in range(2):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert len(self.avatar.effects) == 0
        assert self.avatar.attack_strength == 1

    async def test_multiple_invulnerability_boost_pickup_expiry(self, loop):
        """
        Ensure that each invulnerability boost effect expires at the appropriate time, even if the user stacks up on
        them. One pickup will be at (1,0) and another at (3,0).
        """
        cell_one = self.game.game_state.world_map.get_cell(Location(1, 0))
        cell_two = self.game.game_state.world_map.get_cell(Location(3, 0))
        pickup_created_one = InvulnerabilityPickup(cell_one)
        pickup_created_two = InvulnerabilityPickup(cell_two)

        cell_one.interactable = pickup_created_one
        cell_two.interactable = pickup_created_two

        assert self.avatar.resistance == 0

        # Avatar moves EAST to (1,0) where pickup one is located.
        await self.game.simulation_runner.run_single_turn(
            self.game.avatar_manager.get_player_id_to_serialized_action()
        )

        assert isinstance(list(self.avatar.effects)[0], pickup_created_one.effects[0])
        assert len(self.avatar.effects) == 1
        assert list(self.avatar.effects)[0]._time_remaining == 10
        assert self.avatar.resistance == INVULNERABILITY_RESISTANCE

        # Move twice to the second pickup.
        for i in range(2):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert isinstance(list(self.avatar.effects)[1], pickup_created_two.effects[0])
        assert len(self.avatar.effects) == 2
        assert self.avatar.resistance == INVULNERABILITY_RESISTANCE * 2

        # Eight turns later, we expect the first effect to expire.
        for i in range(8):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert len(self.avatar.effects) == 1
        assert list(self.avatar.effects)[0]._time_remaining == 2
        assert self.avatar.resistance == INVULNERABILITY_RESISTANCE

        # Two turns later, the second pickup expires too.
        for i in range(2):
            await self.game.simulation_runner.run_single_turn(
                self.game.avatar_manager.get_player_id_to_serialized_action()
            )

        assert len(self.avatar.effects) == 0
        assert self.avatar.resistance == 0
