import mock
from unittest import TestCase
from .fake_game_runner import FakeGameRunner
from .dummy_avatar import DummyAvatarManager
from simulation.logs import Logs


class TestLogs(TestCase):

    def test_log_provider_setting_logs(self):
        logs = Logs()
        self.assertEqual(len(logs._logs), 0)

        logs.set_user_logs(user_id=1, logs="test logs")
        self.assertEqual(len(logs._logs), 1)
        self.assertIn(1, logs._logs)
        self.assertEqual(logs._logs[1], "test logs")

    def test_log_provider_getting_logs(self):
        logs = Logs()
        logs.set_user_logs(user_id=1, logs="test logs")

        success_logs = logs.get_user_logs(1)
        failed_logs = logs.get_user_logs(50)

        self.assertEqual(success_logs, "test logs")
        self.assertIsNone(failed_logs)

    def test_turn_manager_calls_set_user_logs(self):
        dummy_avatar_manager = DummyAvatarManager()
        fake_game_runner = FakeGameRunner(player_manager=dummy_avatar_manager)
        fake_game_runner.logs.set_user_logs = mock.MagicMock()

        fake_game_runner.run_single_turn()

        first_call = mock.call(logs='Testing', user_id=1)
        second_call = mock.call(logs='Testing', user_id=2)

        fake_game_runner.logs.set_user_logs.assert_has_calls([first_call, second_call])
