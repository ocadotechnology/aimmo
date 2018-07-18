from unittest import TestCase
from avatar_runner import AvatarRunner
from simulation.action import WaitAction


class TestAvatarRunner(TestCase):

    def test_runner_does_not_crash_on_code_errors(self):
        class Avatar(object):
            def process_avatar_turn(self, world_map, avatar_state):
                assert False
                return None

        runner = AvatarRunner(Avatar())
        action = runner.process_avatar_turn({}, {})
        self.assertIsInstance(action, WaitAction)
