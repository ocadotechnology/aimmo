from kubernetes.client import (
    NetworkingV1beta1Api,
    NetworkingV1beta1IngressBackend,
    NetworkingV1beta1HTTPIngressPath,
    NetworkingV1beta1Ingress,
)

import logging

LOGGER = logging.getLogger(__file__)


class GameIngressManager:
    def __init__(self) -> None:
        self.networking_api = NetworkingV1beta1Api()

    def add_game_path_to_ingress(self, game_name: str):
        path = self._get_path_for_game_name(game_name)

        patch = [{"op": "add", "path": "/spec/rules/0/http/paths/-", "value": path}]

        self.networking_api.patch_namespaced_ingress("aimmo-ingress", "default", patch)

    def remove_game_path_from_ingress(self, game_name: str):
        path = self._get_path_for_game_name(game_name)

        try:
            ingress: NetworkingV1beta1Ingress = (
                self.networking_api.list_namespaced_ingress("default").items[0]
            )
        except IndexError:
            LOGGER.warning("No ingress found to remove path from.")
            return

        paths = ingress.spec.rules[0].http.paths

        try:
            index_to_delete = paths.index(path)
        except ValueError:
            return

        patch = [
            {
                "op": "remove",
                "path": "/spec/rules/0/http/paths/{}".format(index_to_delete),
            }
        ]

        self.networking_api.patch_namespaced_ingress("aimmo-ingress", "default", patch)

    def _get_path_for_game_name(
        self, game_name: str
    ) -> NetworkingV1beta1HTTPIngressPath:
        backend = NetworkingV1beta1IngressBackend(game_name, 80)
        return NetworkingV1beta1HTTPIngressPath(backend, f"/{game_name}(/|$)(.*)")
