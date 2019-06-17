import base64
import logging

import kubernetes
import yaml
from kubernetes.client.rest import ApiException

LOGGER = logging.getLogger(__name__)


class TokenSecretCreator:
    """Creates a kubernetes secret to store a games token."""

    def __init__(self):
        kubernetes.config.load_incluster_config()
        self.api = kubernetes.client.CoreV1Api()

    def create_secret(self, name: str, namespace: str, data: dict):
        """Creates the k8s object."""
        body = kubernetes.client.V1Secret(
            kind="Secret",
            string_data=data,
            metadata=kubernetes.client.V1ObjectMeta(name=name, namespace=namespace),
        )

        try:
            self.api.create_namespaced_secret(namespace, body)
        except ApiException:
            self.api.patch_namespaced_secret(name, namespace, body)
