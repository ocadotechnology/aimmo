from unittest.mock import MagicMock

import pytest
from kubernetes.client import (
    V1IngressBackend,
    V1IngressList,
    V1Ingress,
    V1IngressSpec,
    V1IngressRule,
    V1HTTPIngressRuleValue,
    V1HTTPIngressPath,
    V1IngressServiceBackend,
    V1ServiceBackendPort,
)

from aimmo.game_manager.game_ingress_manager import GameIngressManager


@pytest.fixture
def game_ingress_manager():
    manager = GameIngressManager()
    manager.networking_api = MagicMock()
    return manager


def test_add_game_path_to_ingress(game_ingress_manager: GameIngressManager):
    game_name = "game-123-test"
    game_port = V1ServiceBackendPort(number=80)
    game_service = V1IngressServiceBackend(game_name, game_port)
    backend = V1IngressBackend(service=game_service)
    path = V1HTTPIngressPath(backend, f"/{game_name}(/|$)(.*)", path_type="Prefix")
    expected_patch = [{"op": "add", "path": "/spec/rules/0/http/paths/-", "value": path}]

    game_ingress_manager.add_game_path_to_ingress(game_name)

    game_ingress_manager.networking_api.patch_namespaced_ingress.assert_called_with(
        "aimmo-ingress", "default", expected_patch
    )


def test_remove_game_path_from_ingress(game_ingress_manager: GameIngressManager):
    game_name = "game-123-test"
    path = game_ingress_manager._get_path_for_game_name(game_name)

    game_ingress_manager.networking_api.list_namespaced_ingress.return_value = V1IngressList(
        items=[
            V1Ingress(
                spec=V1IngressSpec(
                    default_backend=path.backend, rules=[V1IngressRule(http=V1HTTPIngressRuleValue(paths=[path]))]
                )
            )
        ]
    )

    expected_patch = [{"op": "remove", "path": "/spec/rules/0/http/paths/0"}]

    game_ingress_manager.remove_game_path_from_ingress(game_name=game_name)

    game_ingress_manager.networking_api.patch_namespaced_ingress.assert_called_with(
        "aimmo-ingress", "default", expected_patch
    )
