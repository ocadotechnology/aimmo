import unittest
from .fake_game_runner import FakeGameRunner


class TestAvatarLocation(unittest.TestCase):

    def test_avatar_location_stays_same_after_code_change(self):
        game_runner = FakeGameRunner()
        game_runner.run_single_turn()
        avatar_location_before_code_change = game_runner.get_avatar(1).location
        game_runner.change_avatar_code(1, "class Avatar: different code")
        game_runner.run_single_turn()
        avatar_location_after_code_change = game_runner.get_avatar(1).location
        self.assertEqual(avatar_location_before_code_change, avatar_location_after_code_change)


