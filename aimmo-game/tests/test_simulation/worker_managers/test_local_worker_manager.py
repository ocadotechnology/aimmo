import os

from unittest import TestCase

from simulation.worker_managers.local_worker_manager import LocalWorkerManager


class TestLocalWorkerManager(TestCase):
    def test_local_worker_ports_do_not_conflict(self):
        os.environ['GAME_ID'] = '1'
        worker_manager1 = LocalWorkerManager()
        local_worker1 = worker_manager1.create_worker(1)
        _, _, port1 = local_worker1.split(':')

        os.environ['GAME_ID'] = '2'
        worker_manager2 = LocalWorkerManager()
        local_worker2 = worker_manager2.create_worker(1)
        _, _, port2 = local_worker2.split(':')

        self.assertNotEquals(port1, port2)

    def test_local_workers_in_the_same_game_do_not_have_port_conflicts(self):
        os.environ['GAME_ID'] = '1'
        worker_manager = LocalWorkerManager()
        local_worker1 = worker_manager.create_worker(1)
        local_worker2 = worker_manager.create_worker(2)
        _, _, port1 = local_worker1.split(':')
        _, _, port2 = local_worker2.split(':')

        self.assertNotEquals(port1, port2)
