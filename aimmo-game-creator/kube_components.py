import logging

import kubernetes
from kubernetes.client.rest import ApiException

LOGGER = logging.getLogger(__name__)


class TokenSecretCreator:
    """Creates a kubernetes secret to store a games token."""

    def __init__(self):
        self.api = kubernetes.client.CoreV1Api()

    def create_secret_object(self, name: str, namespace: str, data: dict):
        return kubernetes.client.V1Secret(
            kind="Secret",
            string_data=data,
            metadata=kubernetes.client.V1ObjectMeta(
                name=name,
                namespace=namespace,
                labels={"game_id": name.split("-")[1], "app": "aimmo-game"},
            ),
        )

    def create_secret(self, name: str, namespace: str, data: dict):
        """Creates the k8s object."""
        body = self.create_secret_object(name, namespace, data)

        try:
            self.api.create_namespaced_secret(namespace, body)
        except ApiException:
            LOGGER.debug(
                "Either we already have a secret, or something has gone wrong."
            )
