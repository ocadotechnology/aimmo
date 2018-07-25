import logging
import os
import time

from pykube import HTTPClient, KubeConfig, Pod
from .worker_manager import WorkerManager

LOGGER = logging.getLogger(__name__)


class KubernetesWorkerManager(WorkerManager):
    """Kubernetes worker manager."""

    def __init__(self, *args, **kwargs):
        self.api = HTTPClient(KubeConfig.from_service_account())
        self.game_id = os.environ['GAME_ID']
        self.game_url = os.environ['GAME_URL']
        super(KubernetesWorkerManager, self).__init__(*args, **kwargs)

    def create_worker(self, player_id):
        pod = Pod(
            self.api,
            {
                'kind': 'Pod',
                'apiVersion': 'v1',
                'metadata': {
                    'generateName': "aimmo-%s-worker-%s-" % (self.game_id, player_id),
                    'labels': {
                        'app': 'aimmo-game-worker',
                        'game': self.game_id,
                        'player': str(player_id),
                    },
                },
                'spec': {
                    'containers': [
                        {
                            'env': [
                                {
                                    'name': 'DATA_URL',
                                    'value': "%s/player/%d" % (self.game_url, player_id),
                                },
                            ],
                            'name': 'aimmo-game-worker',
                            'image': 'ocadotechnology/aimmo-game-worker:%s' % os.environ.get('IMAGE_SUFFIX', 'latest'),
                            'ports': [
                                {
                                    'containerPort': 5000,
                                    'protocol': 'TCP'
                                }
                            ],
                            'resources': {
                                'limits': {
                                    'cpu': '10m',
                                    'memory': '64Mi',
                                },
                                'requests': {
                                    'cpu': '7m',
                                    'memory': '32Mi',
                                },
                            },
                            'securityContext': {
                                'capabilities': {
                                    'drop': [
                                        'all'
                                    ],
                                    'add': [
                                        'NET_BIND_SERVICE'
                                    ]
                                }
                            }
                        },
                    ],
                },
            }
        )
        pod.create()
        iterations = 0
        while pod.obj['status']['phase'] == 'Pending':
            if iterations > 30:
                raise EnvironmentError('Could not start worker %s, details %s' % (player_id, pod.obj))
            LOGGER.debug('Waiting for worker %s', player_id)
            time.sleep(5)
            pod.reload()
            iterations += 1
        worker_url = "http://%s:5000" % pod.obj['status']['podIP']
        LOGGER.info("Worker started for %s, listening at %s", player_id, worker_url)
        return worker_url

    def remove_worker(self, player_id):
        for pod in Pod.objects(self.api).filter(selector={
            'app': 'aimmo-game-worker',
            'game': self.game_id,
            'player': str(player_id),
        }):
            LOGGER.debug('Removing pod %s', pod.obj['spec'])
            pod.delete()
