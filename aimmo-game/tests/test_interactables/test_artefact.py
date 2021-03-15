import pytest

from simulation.action import PickupAction
from simulation.interactables.pickups import Artefact, KeyArtefact, ChestArtefact
from simulation.location import Location
from tests.test_simulation.dummy_avatar import CustomLiveDummy
from .mock_world import MockWorld


testdata = [
    (Artefact, "artefact"),
    (KeyArtefact, "key"),
    (ChestArtefact, "chest"),
]


@pytest.fixture
def game() -> "MockWorld":
    world = MockWorld(dummies_list=[CustomLiveDummy])
    world.simulation_runner.add_avatar(1, Location(0, 0))
    return world


@pytest.fixture
def cell(game):
    return game.game_state.world_map.get_cell(Location(1, 0))


@pytest.mark.parametrize("artefact_class, artefact_type", testdata)
def test_artefact_serialization(cell, artefact_class, artefact_type):
    artefact = artefact_class(cell)
    assert artefact.serialize() == {
        "type": artefact_type,
        "location": {"x": cell.location.x, "y": cell.location.y},
    }

    artefact.in_backpack = True
    assert artefact.serialize() == {"type": artefact_type}


@pytest.mark.asyncio
@pytest.mark.parametrize("artefact_class, artefact_type", testdata)
async def test_artefact_applies_correctly(game, cell, artefact_class, artefact_type):
    avatar: "CustomLiveDummy" = game.avatar_manager.get_avatar(1)
    artefact = artefact_class(cell)
    cell.interactable = artefact

    # Move to the cell with the artefact

    await game.simulation_runner.run_single_turn(
        game.turn_collector.collected_turn_actions
    )

    assert cell.interactable is not None

    # Pickup the artefact

    avatar.set_next_action(PickupAction(avatar))

    await game.simulation_runner.run_single_turn(
        game.turn_collector.collected_turn_actions
    )

    assert cell.avatar == avatar
    assert cell.interactable is None
    assert len(avatar.backpack) == 1
    assert avatar.backpack == [artefact]
