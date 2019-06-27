import asyncio

import pytest
from concrete_worker import ConcreteWorker
from simulation.worker_manager import WorkerManager


@pytest.fixture
def worker_manager():
    worker_manager = WorkerManager()
    worker_manager.worker_class = ConcreteWorker
    worker_manager.add_new_worker(1)
    worker_manager.add_new_worker(2)

    return worker_manager
