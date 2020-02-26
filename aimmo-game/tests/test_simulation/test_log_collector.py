from unittest import TestCase

from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.log_collector import LogCollector
from simulation.workers.worker import Worker
from .mock_worker_manager import MockWorkerManager


class MockWorker(Worker):
    def _create_worker(self):
        pass


class MockAvatarManager(object):
    avatars_by_id = {}

    def add_avatar(self, player_id):
        avatar = AvatarWrapper(player_id, None, None)
        self.avatars_by_id[player_id] = avatar
        return avatar

    def get_avatar(self, user_id):
        return self.avatars_by_id[user_id]


class TestLogCollector(TestCase):
    def test_collect_logs(self):
        worker_manager = MockWorkerManager()
        avatar_manager = MockAvatarManager()

        log_collector = LogCollector(worker_manager, avatar_manager)
        worker = MockWorker(None, None)
        worker.log = "Worker test log"

        worker_manager.player_id_to_worker[1] = worker

        avatar = AvatarWrapper(None, None, None)

        avatar_manager.avatars_by_id[1] = avatar

        log_collector.collect_logs(1)

        self.assertEquals(log_collector.player_logs, "Worker test log")

        avatar.logs.append("Avatar test log")

        log_collector.collect_logs(1)

        self.assertEquals(log_collector.player_logs, "Worker test logAvatar test log")
