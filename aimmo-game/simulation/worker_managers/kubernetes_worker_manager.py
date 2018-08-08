import logging
import os
import time

import kubernetes.client
import kubernetes.config

from .worker_manager import WorkerManager

LOGGER = logging.getLogger(__name__)
K8S_NAMESPACE = 'default'


class KubernetesWorkerManager(WorkerManager):
    """Kubernetes worker manager."""

    def __init__(self, *args, **kwargs):
        kubernetes.config.load_incluster_config()
        self.api = kubernetes.client.CoreV1Api()
        self.game_id = os.environ['GAME_ID']
        self.game_url = os.environ['GAME_URL']
        super(KubernetesWorkerManager, self).__init__(*args, **kwargs)

    def make_pod(self, player_id):
        container = kubernetes.client.V1Container(
                            env=[kubernetes.client.V1EnvVar(
                                         name='DATA_URL',
                                         value='%s/player/%d' % (self.game_url, player_id))],
                            name='aimmo-game-worker',
                            image='ocadotechnology/aimmo-game-worker:%s' % os.environ.get('IMAGE_SUFFIX', 'latest'),
                            ports=[kubernetes.client.V1ContainerPort(
                                            container_port=5000,
                                            protocol='TCP')],
                            resources=kubernetes.client.V1ResourceRequirements(
                                            limits={'cpu': '10m', 'memory': '64Mi'},
                                            requests={'cpu': '7m', 'memory': '32Mi'}),
                            security_context=kubernetes.client.V1SecurityContext(
                                                capabilities=kubernetes.client.V1Capabilities(
                                                    drop=['all'],
                                                    add=['NET_BIND_SERVICE'])))
        pod_manifest = kubernetes.client.V1PodSpec(containers=[container])

        metadata = kubernetes.client.V1ObjectMeta(
                        labels={
                            'app': 'aimmo-game-worker',
                            'game': self.game_id,
                            'player': str(player_id)},
                        generate_name="aimmo-%s-worker-%s-" % (self.game_id, player_id))

        return kubernetes.client.V1Pod(metadata=metadata, spec=pod_manifest)

    def _wait_for_pod_creation(self, pod_name, player_id):

        for _ in range(90):
            pod = self.api.read_namespaced_pod(pod_name, K8S_NAMESPACE)
            LOGGER.info('Pod status: {}'.format(pod.status))
            if pod.status.phase == 'Running':
                return pod

            time.sleep(1)

        raise EnvironmentError('Could not start worker %s.' % player_id)

    def create_worker(self, player_id):
        pod_obj = self.make_pod(player_id)
        LOGGER.info('Making new worker pod: {}'.format(pod_obj.metadata.name))
        pod = self.api.create_namespaced_pod(namespace=K8S_NAMESPACE, body=pod_obj)
        pod_name = pod.metadata.name
        pod = self._wait_for_pod_creation(pod_name, player_id)

        worker_url = 'http://%s:5000' % pod.status.pod_ip
        LOGGER.info('Worker ip: {}'.format(pod.status.pod_ip))
        LOGGER.info('Worker started for %s, listening at %s', player_id, worker_url)
        return worker_url

    def remove_worker(self, player_id):
        app_label = 'app=aimmo-game-worker'
        game_label = 'game={}'.format(self.game_id)
        player_label = 'player={}'.format(player_id)

        pods = self.api.list_namespaced_pod(namespace=K8S_NAMESPACE,
                                            label_selector=','.join([app_label, game_label, player_label]))

        LOGGER.error('Removing pods {}'.format([pod.metadata.name for pod in pods.items]))

        for pod in pods.items:
            LOGGER.error('Pod name: {}'.format(pod.metadata.name))
            self.api.delete_namespaced_pod(pod.metadata.name, K8S_NAMESPACE, kubernetes.client.V1DeleteOptions())
