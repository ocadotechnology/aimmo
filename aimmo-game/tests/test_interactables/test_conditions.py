import asyncio
import math

import pytest
from simulation.location import Location
from simulation.interactables.conditions import TurnState, avatar_on_cell

from .mock_world import MockWorld


@pytest.fixture
def game():
    game = MockWorld()
    game.simulation_runner.add_avatar(1, Location(0, 0))
    return game


def test_avatar_on_cell(game):
    cell = game.game_state.world_map.get_cell(Location(1, 0))
    condition = avatar_on_cell(TurnState(game.game_state.world_map, cell))
    assert not condition

    cell = game.game_state.world_map.get_cell(Location(0, 0))
    condition = avatar_on_cell(TurnState(game.game_state.world_map, cell))
    assert condition
