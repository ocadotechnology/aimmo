from unittest import TestCase

from simulation.worker_managers.local_worker_manager import LocalWorkerManager

class TestLocalWorkerManager(TestCase):
    def test_local_worker_ports_do_not_conflict(self):
        os.environ['GAME_ID'] = 1
        worker_manager1 = LocalWorkerManager()
        local_worker1 = worker_manager1.create_worker(1)

        os.environ['GAME_ID'] = 2
        worker_manager2 = LocalWorkerManager()
        local_worker2 = worker_manager1.create_worker(1)

        assertNotEquals(local_worker1.port, local_worker2.port)