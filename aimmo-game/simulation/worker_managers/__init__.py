from kubernetes_worker_manager import KubernetesWorkerManager
from local_worker_manager import LocalWorkerManager

WORKER_MANAGERS = {
    'local': LocalWorkerManager,
    'kubernetes': KubernetesWorkerManager,
}