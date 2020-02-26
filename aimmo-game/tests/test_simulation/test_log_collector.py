from unittest import TestCase

from simulation.workers.worker import Worker
from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.log_collector import LogCollector


class MockWorker(Worker):
    def _create_worker(self):
        pass


class TestLogCollector(TestCase):
    def test_collect_logs(self):
        log_collector = LogCollector()
        worker = MockWorker(None, None)
        log_collector.worker = worker
        worker.log = "Worker test log"

        avatar = AvatarWrapper(None, None, None)
        log_collector.avatar = avatar

        log_collector.collect_logs()

        self.assertEquals(log_collector.player_logs, "Worker test log")

        avatar.log = "Avatar test log"

        log_collector.collect_logs()

        self.assertEquals(log_collector.player_logs, "Worker test logAvatar test log")
