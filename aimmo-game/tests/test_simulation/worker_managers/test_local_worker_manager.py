import os
import mock

from unittest import TestCase
from urllib.parse import urlparse

from simulation.worker_managers.local_worker_manager import LocalWorkerManager


class TestLocalWorkerManager(TestCase):
    @mock.patch('docker.from_env')
    def test_local_worker_ports_do_not_conflict(self, docker_from_env):
        os.environ['GAME_ID'] = '1'
        worker_manager1 = LocalWorkerManager()
        local_worker1 = worker_manager1.create_worker(1)
        url1 = urlparse(local_worker1)

        os.environ['GAME_ID'] = '2'
        worker_manager2 = LocalWorkerManager()
        local_worker2 = worker_manager2.create_worker(1)
        url2 = urlparse(local_worker2)

        self.assertEqual(url1.port, 11989)
        self.assertEqual(url2.port, 21989)

    @mock.patch('docker.from_env')
    def test_local_workers_in_the_same_game_do_not_have_port_conflicts(self, docker_from_env):
        os.environ['GAME_ID'] = '1'
        worker_manager = LocalWorkerManager()
        local_worker1 = worker_manager.create_worker(1)
        local_worker2 = worker_manager.create_worker(2)
        url1 = urlparse(local_worker1)
        url2 = urlparse(local_worker2)

        self.assertEqual(url1.port, 11989)
        self.assertEqual(url2.port, 11990)
