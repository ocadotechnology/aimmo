import asyncio

import pytest
from simulation.interactables.score_location import ScoreLocation
from simulation.location import Location

from .mock_world import MockWorld

game = None
cell = None


@pytest.fixture
def test_data():
    """
    Mock a game for each test individually. MockWorld() will set up a:
    avatar manager, game state, turn manager and a map generator.
    """
    game = MockWorld()
    game.simulation_runner.add_avatar(1, Location(0, 0))
    cell = game.game_state.world_map.get_cell(Location(0, 0))

    # Avatar will try to move North, so we force it to stay in place
    game.game_state.world_map.get_cell(Location(1, 0)).habitable = False

    return game, cell


def test_score_location_increase_score_of_avatar(test_data):
    """
    Avatar spawns at the origin (0,0) and should have a score of 0. Moves
    EAST to (1,0) and should automatically then receive an effect that will
    increase the avatars score.
    """
    game, cell = test_data
    cell.interactable = ScoreLocation(cell)
    assert game.avatar_manager.get_avatar(1).score is 0
    assert cell.interactable.serialize() == {
        "type": "score",
        "location": {"x": cell.location.x, "y": cell.location.y},
    }

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        game.simulation_runner.run_single_turn(
            game.avatar_manager.get_player_id_to_serialized_action()
        )
    )

    assert cell.avatar is game.avatar_manager.get_avatar(1)
    assert cell.avatar.score is 1
    assert len(cell.avatar.effects) is 1


def test_score_locations_persist_and_keep_giving_score_effects(test_data):
    """
    Checks if score can be increased more than once. First moved from ORIGIN to 1,0 ->
    then is given some score, remains in place due to an obstacle, then next turn
    it's score should increase again.
    """
    game, cell = test_data
    loop = asyncio.get_event_loop()
    cell.interactable = ScoreLocation(cell)
    loop.run_until_complete(
        game.simulation_runner.run_single_turn(
            game.avatar_manager.get_player_id_to_serialized_action()
        )
    )
    assert cell.avatar is game.avatar_manager.get_avatar(1)
    assert cell.avatar.score is 1

    loop.run_until_complete(
        game.simulation_runner.run_single_turn(
            game.avatar_manager.get_player_id_to_serialized_action()
        )
    )

    assert cell.avatar.score is 2
    assert cell.avatar is game.avatar_manager.get_avatar(1)
