import time
from unittest.mock import DEFAULT, MagicMock, PropertyMock

import aimmo.game_manager
import kubernetes
import pytest
from aimmo.game_manager import K8S_NAMESPACE, GameManager
from kubernetes.client.exceptions import ApiException


@pytest.fixture
def game_manager() -> GameManager:
    return GameManager()


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


def test_patch_game_service(game_manager, game_id):
    game_manager.api.patch_namespaced_service = MagicMock()
    game_server_name = "test"
    expected_service = kubernetes.client.V1Service(
        spec=kubernetes.client.V1ServiceSpec(
            selector={"agones.dev/gameserver": game_server_name}
        )
    )

    game_manager.patch_game_service(game_id=game_id, game_server_name=game_server_name)

    game_manager.api.patch_namespaced_service.assert_called_with(
        game_manager.create_game_name(game_id), K8S_NAMESPACE, expected_service
    )


def test_create_game_server_allocation(game_manager, game_id, game_data, monkeypatch):
    monkeypatch.setattr(time, "sleep", MagicMock)
    unallocated_result = {"status": {"state": "UnAllocated"}}
    game_manager.custom_objects_api.create_namespaced_custom_object = MagicMock(
        side_effect=[unallocated_result, DEFAULT]
    )

    game_manager.create_game_server_allocation(game_id=game_id, game_data=game_data)

    game_manager.custom_objects_api.create_namespaced_custom_object.assert_called_with(
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


def test_delete_game_server(game_manager, game_id):
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
    game_manager.custom_objects_api.list_namespaced_custom_object = MagicMock(
        return_value={"items": [mock_game_server, MagicMock()]}
    )
    game_manager.custom_objects_api.delete_namespaced_custom_object = MagicMock()

    game_data = game_manager.delete_game_server(game_id=game_id)

    assert game_data == {"worksheet_id": worksheet_id}


def test_recreate_game_server(game_manager, game_id):
    mock_game_data = MagicMock()
    mock_game_server_name = MagicMock()
    game_manager.delete_game_server = MagicMock(return_value=mock_game_data)
    game_manager.create_game_server_allocation = MagicMock(
        return_value=mock_game_server_name
    )
    game_manager.patch_game_service = MagicMock()

    game_manager.recreate_game_server(game_id=game_id)

    game_manager.delete_game_server.assert_called_with(game_id=game_id)
    game_manager.create_game_server_allocation.assert_called_with(
        game_id=game_id, game_data=mock_game_data
    )
    game_manager.patch_game_service.assert_called_with(
        game_id=game_id, game_server_name=mock_game_server_name
    )


def test_create_game_secret(game_manager, game_id):
    token = "secret-token"
    name = game_manager.create_game_name(game_id) + "-token"
    expected_secret = kubernetes.client.V1Secret(
        kind="Secret",
        string_data={"token": token},
        metadata=kubernetes.client.V1ObjectMeta(
            name=name,
            namespace=K8S_NAMESPACE,
            labels={"game_id": str(game_id), "app": "aimmo-game"},
        ),
    )

    game_manager.api.read_namespaced_secret = MagicMock()
    game_manager.api.create_namespaced_secret = MagicMock()
    game_manager.api.patch_namespaced_secret = MagicMock()
    aimmo.game_manager.LOGGER.exception = MagicMock()

    # Test create secret success
    game_manager.api.read_namespaced_secret.side_effect = ApiException()
    game_manager.create_game_secret(game_id=game_id, token=token)
    game_manager.api.create_namespaced_secret.assert_called_with(
        namespace=K8S_NAMESPACE, body=expected_secret
    )

    # Test create secret exception
    game_manager.api.create_namespaced_secret.side_effect = ApiException()
    game_manager.create_game_secret(game_id=game_id, token=token)
    aimmo.game_manager.LOGGER.exception.assert_called()

    # Test patch secret success
    game_manager.api.read_namespaced_secret.side_effect = None
    game_manager.create_game_secret(game_id=game_id, token=token)
    game_manager.api.patch_namespaced_secret.assert_called_with(
        name=name, namespace=K8S_NAMESPACE, body=expected_secret
    )

    # Test patch secret exception
    game_manager.api.patch_namespaced_secret.side_effect = ApiException()
    game_manager.create_game_secret(game_id=game_id, token=token)
    aimmo.game_manager.LOGGER.exception.assert_called()


def test_delete_game_secret(game_manager, game_id):
    secret_name = "secret1"
    mock_secret = MagicMock()
    mock_secret.metadata.name = secret_name
    game_manager.api.list_namespaced_secret = MagicMock()
    type(game_manager.api.list_namespaced_secret.return_value).items = PropertyMock(
        return_value=[mock_secret]
    )
    game_manager.api.delete_namespaced_secret = MagicMock()

    game_manager.delete_game_secret(game_id=game_id)
    game_manager.api.delete_namespaced_secret.assert_called_with(
        name=secret_name, namespace=K8S_NAMESPACE
    )
