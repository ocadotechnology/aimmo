from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.log_collector import LogCollector
from .mock_avatar_manager import MockAvatarManager
from .mock_worker import MockWorker
from .mock_worker_manager import MockWorkerManager


def test_collect_logs():
    worker_manager = MockWorkerManager()
    avatar_manager = MockAvatarManager()

    log_collector = LogCollector(worker_manager, avatar_manager)
    worker = MockWorker(None, None)
    worker.logs = ["Worker test log"]

    worker_manager.player_id_to_worker[1] = worker

    avatar = AvatarWrapper(None, None, None)

    avatar_manager.avatars_by_id[1] = avatar

    assert log_collector.collect_logs(1) == "Worker test log"

    avatar.logs = ["Avatar test log"]

    assert log_collector.collect_logs(1) == "Worker test log\nAvatar test log"
