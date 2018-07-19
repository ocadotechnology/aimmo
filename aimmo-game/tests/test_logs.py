from unittest import TestCase
from .fake_game_runner import FakeGameRunner

class TestLogs(TestCase):

    def test_initial_individual_avatar_logs_empty(self):
        game_runner = FakeGameRunner()

        logs = game_runner.get_avatar(1).logs

        self.assertEqual(logs, None) # None or empty dictionary? TODO: check

    def test_individual_avatar_logs_same(self):
        # Check that if the code has no prints or errors, then the logs remain the same

        game_runner = FakeGameRunner()

        game_runner.run_single_turn()
        first_turn_logs = game_runner.get_avatar(1).logs


        new_code = "class Avatar(object):\n" \
                              "    def handle_turn(self, world_view, events):\n" \
                              "        from simulation.action import WaitAction\n" \
                              "        action = WaitAction()\n" \
                              "        return action\n"
        game_runner.change_avatar_code(1, new_code)
        game_runner.run_single_turn()
        second_turn_logs = game_runner.get_avatar(1).logs

        self.assertEqual(first_turn_logs, second_turn_logs)

    def test_individual_avatar_logs_contain_print(self):
        game_runner = FakeGameRunner()

        new_code = "class Avatar(object):\n" \
                   "    def handle_turn(self, world_view, events):\n" \
                   "        from simulation.action import WaitAction\n" \
                   "        print(\"New Code\")\n" \
                   "        return WaitAction()\n"
        game_runner.change_avatar_code(1, new_code)
        game_runner.run_single_turn()

        logs = game_runner.get_avatar(1).logs

        print_dict = {'print': 'New Code'} # TODO: Fix key etc etc

        return self.assertDictContainsSubset(print_dict, logs)


    def test_several_avatars_receive_logs(self):
        game_runner = FakeGameRunner()

        game_runner.run_single_turn()

        # TODO: Find where all the logs have been gathered
        # Assert that size matches no of avatars

        gathered_logs = None #TODO: this
        first_avatar_logs = game_runner.get_avatar(1).logs
        second_avatar_logs = game_runner.get_avatar(2).logs

        self.assertIn(first_avatar_logs, gathered_logs)
        self.assertIn(second_avatar_logs, gathered_logs)

