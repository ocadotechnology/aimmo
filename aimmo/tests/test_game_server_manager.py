import time
from unittest.mock import DEFAULT, MagicMock

import pytest
from aimmo.game_manager import K8S_NAMESPACE
from aimmo.game_manager.game_server_manager import GameServerManager

from .test_game_manager import game_data, game_id


@pytest.fixture
def game_server_manager():
    manager = GameServerManager()
    manager.api = MagicMock()
    manager.api_client = MagicMock()
    manager.custom_objects_api = MagicMock()
    return manager


def test_create_game_server_allocation(
    game_server_manager, game_id, game_data, monkeypatch
):
    monkeypatch.setattr(time, "sleep", MagicMock)
    unallocated_result = {"status": {"state": "UnAllocated"}}
    game_server_manager.custom_objects_api.create_namespaced_custom_object = MagicMock(
        side_effect=[unallocated_result, DEFAULT]
    )

    game_server_manager.create_game_server_allocation(
        game_id=game_id, game_data=game_data
    )

    game_server_manager.custom_objects_api.create_namespaced_custom_object.assert_called_with(
        group="allocation.agones.dev",
        version="v1",
        namespace=K8S_NAMESPACE,
        plural="gameserverallocations",
        body={
            "apiVersion": "allocation.agones.dev/v1",
            "kind": "GameServerAllocation",
            "metadata": {"generateName": "game-allocation-"},
            "spec": {
                "required": {"matchLabels": {"agones.dev/fleet": "aimmo-game"}},
                "scheduling": "Packed",
                "metadata": {
                    "labels": {
                        "game-id": str(game_id),
                    },
                    "annotations": game_data,
                },
            },
        },
    )


def test_delete_game_server(game_server_manager, game_id):
    worksheet_id = "2"
    mock_game_server = {
        "metadata": {
            "name": "test",
            "annotations": {
                "agones.dev/sdk-version": "1.12.0",
                "worksheet_id": worksheet_id,
            },
        }
    }
    game_server_manager.custom_objects_api.list_namespaced_custom_object = MagicMock(
        return_value={"items": [mock_game_server, MagicMock()]}
    )

    game_data = game_server_manager.delete_game_server(game_id=game_id)

    assert game_data == {"worksheet_id": worksheet_id}
