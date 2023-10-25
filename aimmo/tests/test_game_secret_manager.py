import logging
from unittest.mock import MagicMock, PropertyMock

import pytest
from aimmo.game_manager import K8S_NAMESPACE
from aimmo.game_manager.game_secret_manager import GameSecretManager
from kubernetes.client import V1ObjectMeta, V1Secret
from kubernetes.client.exceptions import ApiException

from .test_game_manager import game_id


@pytest.fixture
def game_secret_manager() -> GameSecretManager:
    manager = GameSecretManager()
    manager.api = MagicMock()
    manager.api_client = MagicMock()
    manager.custom_objects_api = MagicMock()
    return manager


def test_create_game_secret(game_secret_manager, game_id, caplog: pytest.LogCaptureFixture):
    token = "secret-token"
    secret_name = "game-5-token"
    game_name = "game-5"
    expected_secret = V1Secret(
        kind="Secret",
        string_data={"token": token},
        metadata=V1ObjectMeta(
            name=secret_name,
            namespace=K8S_NAMESPACE,
            labels={"game_id": str(game_id), "app": "aimmo-game"},
        ),
    )

    # Test create secret success
    game_secret_manager.api.read_namespaced_secret.side_effect = ApiException()
    game_secret_manager.create_game_secret(game_id=game_id, game_name=game_name, token=token)
    game_secret_manager.api.create_namespaced_secret.assert_called_with(namespace=K8S_NAMESPACE, body=expected_secret)

    # Test create secret exception
    game_secret_manager.api.create_namespaced_secret.side_effect = ApiException()
    game_secret_manager.create_game_secret(game_id=game_id, game_name=game_name, token=token)
    assert caplog.record_tuples == [
        (
            "aimmo.game_manager.game_secret_manager",
            logging.ERROR,
            "Exception when calling create_namespaced_secret",
        )
    ]
    caplog.clear()

    # Test patch secret success
    game_secret_manager.api.read_namespaced_secret.side_effect = None
    game_secret_manager.create_game_secret(game_id=game_id, game_name=game_name, token=token)
    game_secret_manager.api.patch_namespaced_secret.assert_called_with(
        name=secret_name, namespace=K8S_NAMESPACE, body=expected_secret
    )

    # Test patch secret exception
    game_secret_manager.api.patch_namespaced_secret.side_effect = ApiException()
    game_secret_manager.create_game_secret(game_id=game_id, game_name=game_name, token=token)
    assert caplog.record_tuples == [
        (
            "aimmo.game_manager.game_secret_manager",
            logging.ERROR,
            "Exception when calling patch_namespaced_secret",
        )
    ]


def test_delete_game_secret(game_secret_manager: GameSecretManager, game_id: int):
    secret_name = "secret1"
    mock_secret = MagicMock()
    mock_secret.metadata.name = secret_name
    type(game_secret_manager.api.list_namespaced_secret.return_value).items = PropertyMock(return_value=[mock_secret])

    game_secret_manager.delete_game_secret(game_id=game_id)
    game_secret_manager.api.delete_namespaced_secret.assert_called_with(name=secret_name, namespace=K8S_NAMESPACE)
