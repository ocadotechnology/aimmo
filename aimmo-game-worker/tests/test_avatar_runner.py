from unittest import TestCase
import json
from avatar_runner import AvatarRunner
from simulation.action import WaitAction


class TestAvatarRunner(TestCase):

    def test_runner_does_not_crash_on_code_errors(self):
        class Avatar(object):
            def handle_turn(self, world_map, avatar_state):
                assert False
                return None

        runner = AvatarRunner(Avatar())
        action = runner.handle_turn({}, {})
        self.assertIsInstance(action, WaitAction)
