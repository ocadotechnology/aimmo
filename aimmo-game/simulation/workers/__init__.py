from .kubernetes_worker import KubernetesWorker as _KWorker
from .local_worker import LocalWorker as _LWorker

WORKER = {"local": _LWorker, "kubernetes": _KWorker}
