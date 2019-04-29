import logging
import os
import time

from kubernetes import client
from kubernetes import config

from .worker import Worker

LOGGER = logging.getLogger(__name__)
# Default here to stop import errors if imported when running locally
K8S_NAMESPACE = os.environ.get("K8S_NAMESPACE", "")


class KubernetesWorker(Worker):
    """Kubernetes worker."""

    def __init__(self, *args, **kwargs):
        config.load_incluster_config()
        self.api = client.CoreV1Api()
        self.game_id = os.environ["GAME_ID"]
        self.game_url = os.environ["GAME_URL"]
        self.pod_name = os.environ["POD_NAME"]
        super(KubernetesWorker, self).__init__(*args, **kwargs)

    @staticmethod
    def _create_a_label_selector_from_labels(label_list):
        return ",".join(label_list)

    def _make_owner_references(self):
        try:
            return [
                client.V1OwnerReference(
                    api_version="v1",
                    block_owner_deletion=True,
                    controller=True,
                    kind="Pod",
                    name=self.pod_name,
                    uid=self._get_game_uid(),
                )
            ]
        except IndexError:
            # Couldn't find the current pod
            return []

    def _make_container(self, player_id):
        return client.V1Container(
            env=[
                client.V1EnvVar(
                    name="DATA_URL", value="%s/player/%d" % (self.game_url, player_id)
                ),
                client.V1EnvVar(name="PORT", value="5000"),
            ],
            name="aimmo-game-worker",
            image="ocadotechnology/aimmo-game-worker:%s"
            % os.environ.get("IMAGE_SUFFIX", "latest"),
            ports=[client.V1ContainerPort(container_port=5000, protocol="TCP")],
            resources=client.V1ResourceRequirements(
                limits={"cpu": "10m", "memory": "64Mi"},
                requests={"cpu": "6m", "memory": "32Mi"},
            ),
            security_context=client.V1SecurityContext(
                capabilities=client.V1Capabilities(
                    drop=["all"], add=["NET_BIND_SERVICE"]
                )
            ),
        )

    def make_pod(self):
        pod_manifest = client.V1PodSpec(
            containers=[self._make_container(self.player_id)],
            service_account_name="worker",
        )

        metadata = client.V1ObjectMeta(
            labels={
                "app": "aimmo-game-worker",
                "game": self.game_id,
                "player": str(self.player_id),
            },
            generate_name="aimmo-%s-worker-%s-" % (self.game_id, self.player_id),
            owner_references=self._make_owner_references(),
        )
        return client.V1Pod(metadata=metadata, spec=pod_manifest)

    def _get_game_uid(self):
        pod_list = self.api.list_namespaced_pod(
            namespace=K8S_NAMESPACE, field_selector=f"metadata.name={self.pod_name}"
        )
        pod_metadata = pod_list.items[0].metadata
        return pod_metadata.uid

    def _wait_for_pod_creation(self, pod_name, player_id):

        for _ in range(90):
            pod = self.api.read_namespaced_pod(pod_name, K8S_NAMESPACE)
            LOGGER.info("Pod status: {}".format(pod.status))
            if pod.status.phase == "Running":
                return pod

            time.sleep(1)

        raise EnvironmentError("Could not start worker %s." % player_id)

    def _create_worker(self):
        pod_obj = self.make_pod()
        LOGGER.info("Making new workers pod: {}".format(pod_obj.metadata.name))
        pod = self.api.create_namespaced_pod(namespace=K8S_NAMESPACE, body=pod_obj)
        pod_name = pod.metadata.name
        pod = self._wait_for_pod_creation(pod_name, self.player_id)

        worker_url = "http://%s:5000" % pod.status.pod_ip
        LOGGER.info("Worker ip: {}".format(pod.status.pod_ip))
        LOGGER.info(
            "Worker started for %s, listening at %s", self.player_id, worker_url
        )
        return worker_url

    def remove_worker(self):
        app_label = "app=aimmo-game-worker"
        game_label = "game={}".format(self.game_id)
        player_label = "player={}".format(self.player_id)
        label_selector = self._create_a_label_selector_from_labels(
            [app_label, game_label, player_label]
        )
        pods = self.api.list_namespaced_pod(
            namespace=K8S_NAMESPACE, label_selector=label_selector
        )

        for pod in pods.items:
            LOGGER.info("Deleting pod: {}".format(pod.metadata.name))
            self.api.delete_namespaced_pod(
                pod.metadata.name, K8S_NAMESPACE, client.V1DeleteOptions()
            )
