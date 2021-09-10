from unittest.mock import MagicMock

import pytest
from aimmo.game_manager import GameManager


@pytest.fixture
def game_manager() -> GameManager:
    return GameManager(
        game_service_manager=MagicMock(),
        game_server_manager=MagicMock(),
        game_secret_manager=MagicMock(),
        game_ingress_manager=MagicMock(),
    )


@pytest.fixture
def game_id() -> int:
    return 5


@pytest.fixture
def game_data() -> dict:
    return {
        "worksheet_id": "1",
        "class_id": "3",
        "era": "1",
        "status": "r",
    }


def test_create_game_name(game_manager, game_id):
    assert game_manager.create_game_name(game_id) == f"game-{game_id}"


def test_create_game_server(game_manager: GameManager, game_id, game_data):
    game_server_name = "test_game_server"
    game_name = game_manager.create_game_name(game_id=game_id)
    game_manager.game_server_manager.create_game_server_allocation.return_value = (
        game_server_name
    )

    game_manager.create_game_server(
        game_id=game_id,
        game_data=game_data,
    )

    game_manager.game_server_manager.create_game_server_allocation.assert_called_with(
        game_id=game_id,
        game_data=game_data,
    )
    game_manager.game_service_manager.create_game_service.assert_called_with(
        game_id=game_id,
        game_name=game_name,
        game_server_name=game_server_name,
    )
    game_manager.game_ingress_manager.add_game_path_to_ingress.assert_called_with(
        game_name=game_name,
    )


def test_delete_game_server(game_manager: GameManager, game_id):
    game_manager.delete_game_server(game_id=game_id)
    game_manager.game_server_manager.delete_game_server.assert_called_with(
        game_id=game_id
    )


def test_recreate_game_server(game_manager: GameManager, game_id):
    mock_game_data = MagicMock()
    mock_game_server_name = MagicMock()
    game_name = game_manager.create_game_name(game_id=game_id)
    game_manager.delete_game_server = MagicMock(return_value=mock_game_data)
    game_manager.game_server_manager.create_game_server_allocation = MagicMock(
        return_value=mock_game_server_name
    )

    game_manager.recreate_game_server(game_id=game_id)

    game_manager.delete_game_server.assert_called_with(game_id=game_id)
    game_manager.game_server_manager.create_game_server_allocation.assert_called_with(
        game_id=game_id, game_data=mock_game_data
    )
    game_manager.game_service_manager.patch_game_service.assert_called_with(
        game_id=game_id, game_name=game_name, game_server_name=mock_game_server_name
    )
