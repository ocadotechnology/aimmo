from typing import TYPE_CHECKING
import pytest
import asyncio
import random

from simulation.location import Location
from simulation.action import PickupAction
from simulation.event import PickedUpEvent
from simulation.interactables.pickups import Artefact


from .mock_world import MockWorld
from tests.test_simulation.dummy_avatar import CustomLiveDummy

if TYPE_CHECKING:
    from simulation.cell import Cell
    from simulation.avatar.avatar_wrapper import AvatarWrapper


@pytest.fixture
def game() -> "MockWorld":
    world = MockWorld(dummies_list=[CustomLiveDummy])
    world.simulation_runner.add_avatar(1, Location(0, 0))
    return world


@pytest.fixture
def cell(game):
    return game.game_state.world_map.get_cell(Location(1, 0))


def test_artefact_serialization(cell):
    artefact = Artefact(cell)
    assert artefact.serialize() == {
        "type": "artefact",
        "location": {"x": cell.location.x, "y": cell.location.y},
    }


@pytest.mark.asyncio
async def test_artefact_applies_correctly(game, cell):
    avatar: "CustomLiveDummy" = game.avatar_manager.get_avatar(1)
    cell.interactable = Artefact(cell)

    # Move to the cell with the artefact

    await game.simulation_runner.run_single_turn(
        game.avatar_manager.get_player_id_to_serialized_action()
    )

    assert cell.interactable is not None

    # Pickup the artefact

    avatar.set_next_action(PickupAction(avatar))

    await game.simulation_runner.run_single_turn(
        game.avatar_manager.get_player_id_to_serialized_action()
    )

    assert cell.avatar == avatar
    assert cell.interactable is None
    assert avatar.number_of_artefacts == 1
