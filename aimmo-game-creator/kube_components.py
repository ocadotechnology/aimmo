import kubernetes
import yaml


class TokenSecretCreator:
    """Creates a kubernetes secret to store a games token."""

    def __init__(self, name: str, namespace: str, data: dict):
        self.name = name
        self.namespace = namespace
        self.data = data
        self.api = kubernetes.client.CoreV1Api()

        self.create_secret()

    def create_secret(self):
        """Loads a template file, fills in the needed data, and creates the k8s object."""
        with open("kube_templates/game_token.yaml", "r") as f:
            template = yaml.safe_load(f)

            template["metadata"]["name"] = self.name
            template["metadata"]["namespace"] = self.namespace
            template["data"]["token"] = self.data["token"]

            metadata = kubernetes.client.V1ObjectMeta(template["metadata"])
            data = template["data"]

            body = kubernetes.client.V1Secret(template)
            self.api.create_namespaced_secret(self.namespace, body)
