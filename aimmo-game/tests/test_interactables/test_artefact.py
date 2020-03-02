import pytest

from simulation.action import PickupAction
from simulation.interactables.pickups import Artefact
from simulation.location import Location
from tests.test_simulation.dummy_avatar import CustomLiveDummy
from .mock_world import MockWorld


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

    artefact.in_backpack = True
    assert artefact.serialize() == {"type": "artefact"}


@pytest.mark.asyncio
async def test_artefact_applies_correctly(game, cell):
    avatar: "CustomLiveDummy" = game.avatar_manager.get_avatar(1)
    artefact = Artefact(cell)
    cell.interactable = artefact

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
    assert len(avatar.backpack) == 1
    assert avatar.backpack == [artefact]
