from .kubernetes_worker_manager import KubernetesWorkerManager as _KWorkerManager
from .local_worker_manager import LocalWorkerManager as _LWorkerManager

WORKER_MANAGERS = {
    'local': _LWorkerManager,
    'kubernetes': _KWorkerManager,
}
