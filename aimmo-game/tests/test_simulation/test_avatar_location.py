import unittest
from .fake_game_runner import FakeGameRunner


class TestAvatarLocation(unittest.TestCase):

    def test_avatar_location_stays_same_after_code_change(self):
        game_runner = FakeGameRunner()
        new_code = "class Avatar(object):\n" \
                   "    def handle_turn(self, world_view, events):\n" \
                   "        from simulation.action import WaitAction\n" \
                   "        print(\"New Code\")\n" \
                   "        return WaitAction()\n"

        game_runner.run_single_turn()
        avatar_location_before_code_change = game_runner.get_avatar(1).location

        game_runner.change_avatar_code(1, new_code)
        game_runner.run_single_turn()
        avatar_location_after_code_change = game_runner.get_avatar(1).location

        self.assertEqual(avatar_location_before_code_change, avatar_location_after_code_change)
