from unittest import TestCase
from .fake_game_runner import FakeGameRunner
from .dummy_avatar import DummyAvatarManager


class TestLogs(TestCase):

    def test_individual_avatar_successfully_receives_logs(self):
        player_manager = DummyAvatarManager()
        game_runner = FakeGameRunner(player_manager=player_manager)
        game_runner.run_single_turn()
        logs = game_runner.get_avatar(1).logs
        self.assertEqual(logs, "Testing")

    def test_several_avatars_successfully_receive_logs(self):
        player_manager = DummyAvatarManager()
        player_manager.add_avatar(1, "", None)
        player_manager.add_avatar(2, "", None)
        game_runner = FakeGameRunner(player_manager=player_manager)
        game_runner.run_single_turn()
        first_avatar_logs = game_runner.get_avatar(1).logs
        second_avatar_logs = game_runner.get_avatar(2).logs
        self.assertEqual(first_avatar_logs, "Testing")
        self.assertEqual(second_avatar_logs, "Testing")
