import logging

import kubernetes
from kubernetes.client import CoreV1Api
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient

from .constants import K8S_NAMESPACE

LOGGER = logging.getLogger(__name__)


class GameServiceManager:
    def __init__(self) -> None:
        self.api: CoreV1Api = CoreV1Api()
        self.api_client: ApiClient = ApiClient()
        self.custom_objects_api: CustomObjectsApi = CustomObjectsApi(self.api_client)

    def create_game_service(self, game_id, game_name, game_server_name):
        LOGGER.info(f"Creating service for game {game_id}")
        service_manifest = kubernetes.client.V1ServiceSpec(
            selector={"agones.dev/gameserver": game_server_name},
            ports=[kubernetes.client.V1ServicePort(name="tcp", protocol="TCP", port=80, target_port=5000)],
        )

        service_metadata = kubernetes.client.V1ObjectMeta(
            name=game_name,
            labels={"app": "aimmo-game", "game_id": f"{game_id}"},
        )

        service = kubernetes.client.V1Service(metadata=service_metadata, spec=service_manifest)
        self.api.create_namespaced_service(K8S_NAMESPACE, service)

    def delete_game_service(self, game_id):
        LOGGER.info(f"Deleting game service for game {game_id}")
        app_label = "app=aimmo-game"
        game_label = "game_id={}".format(game_id)

        resources = self.api.list_namespaced_service(
            namespace=K8S_NAMESPACE, label_selector=",".join([app_label, game_label])
        )

        for resource in resources.items:
            LOGGER.info("Removing service: {}".format(resource.metadata.name))
            try:
                self.api.delete_namespaced_service(resource.metadata.name, K8S_NAMESPACE)
            except Exception as e:
                LOGGER.exception(e)
