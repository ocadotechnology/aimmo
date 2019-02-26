import pytest
from hypothesis import given, assume
from hypothesis import strategies as st
import math
import asyncio

from .mock_world import MockWorld
from simulation.location import Location
from simulation.cell import Cell
from simulation.pickups.pickup_conditions import avatar_on_cell, TurnState


@pytest.fixture
def game():
    game = MockWorld()
    game.game_state.add_avatar(1, Location(0, 0))
    return game

def test_avatar_on_cell(game):
    cell = game.game_state.world_map.get_cell(Location(1, 0))
    condition = avatar_on_cell(TurnState(game.game_state.world_map, cell))
    assert not condition

    cell = game.game_state.world_map.get_cell(Location(0, 0))
    condition = avatar_on_cell(TurnState(game.game_state.world_map, cell))
    assert condition