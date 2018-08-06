import logging
import os
import time

from pykube import HTTPClient, KubeConfig, Pod
from kubernetes import client

from .worker_manager import WorkerManager

LOGGER = logging.getLogger(__name__)
K8S_NAMESPACE = 'default'


class KubernetesWorkerManager(WorkerManager):
    """Kubernetes worker manager."""

    def __init__(self, *args, **kwargs):
        #self.api = HTTPClient(KubeConfig.from_service_account())
        self.api = client.CoreV1Api()
        self.game_id = os.environ['GAME_ID']
        self.game_url = os.environ['GAME_URL']
        super(KubernetesWorkerManager, self).__init__(*args, **kwargs)

    def make_pod(self, player_id):
        container = client.V1Container(
                            env=[client.V1EnvVar(
                                         name='DATA_URL',
                                         value='%s/player/%d' % (self.game_url, player_id))],
                            name='aimmo-game-worker',
                            image='ocadotechnology/aimmo-game-worker:%s' % os.environ.get('IMAGE_SUFFIX', 'latest'),
                            ports=[client.V1ContainerPort(
                                            containerPort=5000,
                                            protocol='TCP')],
                            resources=client.V1ResourceRequirements(
                                    limits={'cpu': '10m', 'memory': '64Mi'},
                                    requests={'cpu': '7m', 'memory': '32Mi'}),
                            securityContext=client.V1SecurityContext(
                                    capabilities=client.V1Capabilities(
                                        drop=['all'],
                                        add=['NET_BIND_SERVICE'])))
        pod_spec = client.V1PodSpec(containers=[container])

        metadata = client.V1ObjectMeta(
                        labels={
                            'app': 'aimmo-game-worker',
                            'game': self.game_id,
                            'player': str(player_id)},
                        generate_name="aimmo-%s-worker-%s-" % (self.game_id, player_id))

        return client.V1Pod(metadata=metadata, spec=pod_spec)

    def create_worker(self, player_id):
        pod = self.api.create_namespace_pod(namespace=K8S_NAMESPACE, body=self.make_pod(player_id))

        iterations = 0
        while pod.status.phase == 'Pending':
            if iterations > 30:
                raise EnvironmentError('Could not start worker %s, details %s' % (player_id, pod.obj))
            LOGGER.debug('Waiting for worker %s', player_id)
            time.sleep(5)
            iterations += 1
        worker_url = "http://%s:5000" % pod.status.pod_ip
        LOGGER.info("Worker started for %s, listening at %s", player_id, worker_url)
        return worker_url

    def remove_worker(self, player_id):
        pods = self.api.list_namespaced_pod(namespace=K8S_NAMESPACE,
                                            selector='''
                                                    'app': 'aimmo-game-worker',
                                                    'game': self.game_id,
                                                    'player': {}'''.format(
                                                    str(player_id)))

        for pod in pods:
            LOGGER.debug('Removing pod %s', pod.spec)
            self.api.delete_namespaced_pod(pod.spec.name, K8S_NAMESPACE, client.V1DeleteOptions())
