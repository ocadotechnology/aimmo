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

    def load_template(self, name: str, namespace: str, data: dict):
        """Creates the template dict, fills in the needed data."""
        template = {}

        template["kind"] = "Secret"

        template["metadata"] = {}
        template["metadata"]["name"] = name
        template["metadata"]["namespace"] = namespace

        template["string_data"] = {}
        template["string_data"]["token"] = data["token"]

        return template

    def create_secret(self, name: str, namespace: str, data: dict):
        """Creates the k8s object."""
        template = self.load_template(name, namespace, data)

        template["metadata"] = kubernetes.client.V1ObjectMeta(**template["metadata"])
        LOGGER.debug(f"Your template sir: {template}")
        body = kubernetes.client.V1Secret(**template)
        LOGGER.debug(f"every body, yeah! {body}")
        try:
            self.api.create_namespaced_secret(namespace, body)
        except ApiException:
            self.api.patch_namespaced_secret(name, namespace, body)
