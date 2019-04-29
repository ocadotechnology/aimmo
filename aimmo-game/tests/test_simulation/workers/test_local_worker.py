import os
import mock

from unittest import TestCase
from urllib.parse import urlparse

from simulation.workers.local_worker import LocalWorker
from simulation.worker_manager import WorkerManager


class TestLocalWorker(TestCase):
    @mock.patch("docker.from_env")
    def test_local_worker_ports_do_not_conflict(self, docker_from_env):
        os.environ["GAME_ID"] = "1"
        LocalWorker._init_port_counter()
        worker_manager1 = WorkerManager()
        worker_manager1.add_new_worker(1)
        local_worker1 = worker_manager1.player_id_to_worker[1]
        url1 = urlparse(local_worker1.url)

        os.environ["GAME_ID"] = "2"
        LocalWorker._init_port_counter()
        worker_manager2 = WorkerManager()
        worker_manager2.add_new_worker(1)
        local_worker2 = worker_manager2.player_id_to_worker[1]
        url2 = urlparse(local_worker2.url)

        self.assertEqual(url1.port, 11989)
        self.assertEqual(url2.port, 21989)

    @mock.patch("docker.from_env")
    def test_local_worker_in_the_same_game_do_not_have_port_conflicts(
        self, docker_from_env
    ):
        os.environ["GAME_ID"] = "1"
        LocalWorker._init_port_counter()
        worker_manager = WorkerManager()
        worker_manager.add_new_worker(1)
        worker_manager.add_new_worker(2)
        local_worker1 = worker_manager.player_id_to_worker[1]
        local_worker2 = worker_manager.player_id_to_worker[2]

        url1 = urlparse(local_worker1.url)
        url2 = urlparse(local_worker2.url)

        self.assertEqual(url1.port, 11989)
        self.assertEqual(url2.port, 11990)
