from kubernetes.client import CoreV1Api, V1Secret, V1ObjectMeta
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient
from kubernetes.client.rest import ApiException

from .constants import K8S_NAMESPACE
import logging

LOGGER = logging.getLogger(__name__)

class GameSecretManager:
    def __init__(self) -> None:
        self.api: CoreV1Api = CoreV1Api()
        self.api_client: ApiClient = ApiClient()
        self.custom_objects_api: CustomObjectsApi = CustomObjectsApi(self.api_client)

    def create_game_secret(self, game_id: int, game_name: str, token: str):
        name = f"{game_name}-token"
        body = V1Secret(
            kind="Secret",
            string_data={"token": token},
            metadata=V1ObjectMeta(
                name=name,
                namespace=K8S_NAMESPACE,
                labels={"game_id": str(game_id), "app": "aimmo-game"},
            ),
        )
        try:
            self.api.read_namespaced_secret(name, K8S_NAMESPACE)
        except ApiException:
            try:
                self.api.create_namespaced_secret(namespace=K8S_NAMESPACE, body=body)
            except ApiException:
                LOGGER.exception("Exception when calling create_namespaced_secret")
        else:
            try:
                self.api.patch_namespaced_secret(
                    name=name, namespace=K8S_NAMESPACE, body=body
                )
            except ApiException:
                LOGGER.exception("Exception when calling patch_namespaced_secret")

    def delete_game_secret(self, game_id: int):
        app_label = "app=aimmo-game"
        game_label = "game_id={}".format(game_id)

        resources = self.api.list_namespaced_secret(
            namespace=K8S_NAMESPACE, label_selector=",".join([app_label, game_label])
        )

        for resource in resources.items:
            LOGGER.info("Removing game secret: {}".format(resource.metadata.name))
            self.api.delete_namespaced_secret(
                name=resource.metadata.name, namespace=K8S_NAMESPACE
            )