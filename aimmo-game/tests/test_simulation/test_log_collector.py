from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.log_collector import LogCollector
from .mock_avatar_manager import MockAvatarManager
from .mock_worker import MockWorker
from .mock_worker_manager import MockWorkerManager


def test_collect_logs():
    avatar_manager = MockAvatarManager()

    log_collector = LogCollector(avatar_manager)

    avatar = AvatarWrapper(None, None, None)

    avatar_manager.avatars_by_id[1] = avatar

    assert log_collector.collect_logs(1) == ""

    avatar.logs = ["Avatar test log"]

    assert log_collector.collect_logs(1) == "Avatar test log"
