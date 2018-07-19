from unittest import TestCase
from avatar_runner import AvatarRunner

class TestLogs(TestCase):

    def test_logs_collected_from_print(self):
        class Avatar(object):
            def handle_turn(self, world_map, avatar_state):
                print "HELLO"
                return None

        runner = AvatarRunner(Avatar())
        _, logs = runner.process_avatar_turn(world_map={}, avatar_state={})
        self.assertIn("HELLO", logs)


    def test_logs_collected_from_errors(self):
        class Avatar(object):
            def handle_turn(self, world_map, avatar_state):
                assert False
                return None

        runner = AvatarRunner(Avatar())
        _, logs = runner.process_avatar_turn(world_map={}, avatar_state={})
        self.assertIn("AssertionError", logs)
