import kubernetes
import yaml


class TokenSecretCreator:
    def __init__(self, name: str, namespace: str, data: dict):
        self.name = name
        self.namespace = namespace
        self.data = data
        self.api = kubernetes.client.CoreV1Api()

        self.create_secret()

    def create_secret(self):
        with open("kube_templates/game_token.yaml", "r") as f:
            template = yaml.safe_load(f)

            template["metadata"]["name"] = self.name
            template["metadata"]["namespace"] = self.namespace
            template["data"]["token"] = data["token"]

            metadata = kubernetes.client.V1ObjectMeta(template["metadata"])
            data = template["data"]

            body = kubernetes.client.V1Secret(data=data, metadata=metadata)
            self.api.create_namespaced_secret(self.namespace, body)
