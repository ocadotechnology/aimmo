import logging

import kubernetes
import yaml
from kubernetes.client.rest import ApiException

LOGGER = logging.Logger(__name__)


class TokenSecretCreator:
    """Creates a kubernetes secret to store a games token."""

    def __init__(self):
        kubernetes.config.load_incluster_config()
        self.api = kubernetes.client.CoreV1Api()

    def load_template(self, name: str, namespace: str, data: dict):
        """Loads a template file, fills in the needed data."""
        with open("kube_templates/game_token.yaml", "r") as f:
            template = yaml.safe_load(f)

            template["metadata"]["name"] = name
            template["metadata"]["namespace"] = namespace
            template["data"]["token"] = data["token"]

            return template

    def create_secret(self, name: str, namespace: str, data: dict):
        """Creates the k8s object."""
        template = self.load_template(name, namespace, data)

        template["metadata"] = kubernetes.client.V1ObjectMeta(template["metadata"])

        body = kubernetes.client.V1Secret(**template)
        LOGGER.debug(f"Secret object to create: {body}")
        try:
            self.api.create_namespaced_secret(namespace, body)
        except ApiException:
            self.api.patch_namespaced_secret(name, namespace, body)
