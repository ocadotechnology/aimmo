from unittest import TestCase
from avatar_runner import AvatarRunner
from simulation.action import WaitAction


class TestAvatarRunner(TestCase):

    def test_runner_does_not_crash_on_code_errors(self):
        class Avatar(object):
            def handle_turn(self, world_map, avatar_state):
                assert False
                return None

        runner = AvatarRunner(Avatar())
        action, logs = runner.process_avatar_turn(world_map={}, avatar_state={})
        self.assertEqual(action, {'action_type': 'wait'})
