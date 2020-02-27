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
    worker.log = "Worker test log"

    worker_manager.player_id_to_worker[1] = worker

    avatar = AvatarWrapper(None, None, None)

    avatar_manager.avatars_by_id[1] = avatar

    log_collector.collect_logs(1)

    assert log_collector.player_logs == "Worker test log"

    avatar.logs.append("Avatar test log")

    log_collector.collect_logs(1)

    assert log_collector.player_logs == "Worker test logAvatar test log"
