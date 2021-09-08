from unittest.mock import MagicMock

import kubernetes
import pytest
from game_manager import K8S_NAMESPACE
from game_manager.game_service_manager import GameServiceManager
from kubernetes.client import V1ObjectMeta, V1Service, V1ServiceList, V1ServiceSpec

from .test_game_manager import game_id


@pytest.fixture
def game_service_manager():
    manager = GameServiceManager()
    manager.api = MagicMock()
    manager.api_client = MagicMock()
    manager.custom_objects_api = MagicMock()
    return manager


def test_create_game_service(game_service_manager: GameServiceManager, game_id):
    game_name = "test-game-name"
    game_server_name = "test-game-server"
    expected_service_spec = V1Service(
        metadata=V1ObjectMeta(
            name=game_name, labels={"app": "aimmo-game", "game_id": game_id}
        ),
        spec=V1ServiceSpec(
            selector={"agones.dev/gameserver": game_server_name},
            ports=[
                kubernetes.client.V1ServicePort(
                    name="tcp", protocol="TCP", port=80, target_port=5000
                )
            ],
        ),
    )
    game_service_manager.create_game_service(
        game_id=game_id,
        game_name=game_name,
        game_server_name=game_server_name,
    )

    game_service_manager.api.create_namespaced_service.assert_called_with(
        K8S_NAMESPACE,
        expected_service_spec,
    )


def test_delete_game_service(game_service_manager: GameServiceManager, game_id):
    test_resource_name = "test-game-service"
    game_service_manager.api.list_namespaced_service.return_value = V1ServiceList(
        items=[
            V1Service(
                metadata=V1ObjectMeta(name=test_resource_name),
            )
        ]
    )

    game_service_manager.delete_game_service(game_id=game_id)

    game_service_manager.api.delete_namespaced_service.assert_called_with(
        test_resource_name,
        K8S_NAMESPACE,
    )


def test_patch_game_service(game_service_manager: GameServiceManager, game_id):
    game_name = "test-game-name"
    game_server_name = "test"
    expected_service = V1Service(
        spec=V1ServiceSpec(selector={"agones.dev/gameserver": game_server_name})
    )

    game_service_manager.patch_game_service(
        game_id=game_id,
        game_name=game_name,
        game_server_name=game_server_name,
    )

    game_service_manager.api.patch_namespaced_service.assert_called_with(
        game_name, K8S_NAMESPACE, expected_service
    )
