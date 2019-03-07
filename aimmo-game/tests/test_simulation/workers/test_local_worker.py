import os
import mock

from unittest import TestCase
from urllib.parse import urlparse

from simulation.workers.local_worker import LocalWorker


class TestLocalWorker(TestCase):
    @mock.patch('docker.from_env')
    def test_local_worker_ports_do_not_conflict(self, docker_from_env):
        os.environ['GAME_ID'] = '1'
        worker1 = LocalWorker(1)
        url1 = urlparse(worker1)

        os.environ['GAME_ID'] = '2'
        worker2 = LocalWorker(2)
        url2 = urlparse(worker2)

        self.assertEqual(url1.port, 11989)
        self.assertEqual(url2.port, 21989)

    @mock.patch('docker.from_env')
    def test_local_workers_in_the_same_game_do_not_have_port_conflicts(self, docker_from_env):
        os.environ['GAME_ID'] = '1'
        worker1 = LocalWorker(1)
        worker2 = LocalWorker(2)

        url1 = urlparse(worker1)
        url2 = urlparse(worker2)

        self.assertEqual(url1.port, 11989)
        self.assertEqual(url2.port, 11990)
