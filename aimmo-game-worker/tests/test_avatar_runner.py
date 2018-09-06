from unittest import TestCase

import mock

from avatar_runner import AvatarRunner
from user_exceptions import InvalidActionException

NORTH = {'x': 0, 'y': 1}
SOUTH = {'x': 0, 'y': -1}
EAST = {'x': 1, 'y': 0}
WEST = {'x': -1, 'y': 0}


class TestAvatarRunner(TestCase):
    def test_runner_does_not_crash_on_code_errors(self):
        class Avatar(object):
            def handle_turn(self, world_map, avatar_state):
                assert False

        runner = AvatarRunner(avatar=Avatar(), auto_update=False)
        action = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code='')['action']
        self.assertEqual(action, {'action_type': 'wait'})

    def test_runner_updates_code_on_change(self):
        avatar1 = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import EAST
                            
                            return MoveAction(EAST)
                  '''
        avatar2 = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import WEST
                            
                            return MoveAction(WEST)
                  '''

        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertEqual(response['action'], {'action_type': 'move', 'options': {'direction': EAST}})

        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)

        self.assertEqual(response['action'], {'action_type': 'move', 'options': {'direction': WEST}})

    def test_runner_can_maintain_state(self):
        """ This test ensures that if the code is the same, we do not recreate the avatar object in the runner.
            We check this by making sure that self.x is being updated and its value retained. """

        avatar = '''class Avatar(object):
                        def __init__(self):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH, SOUTH, EAST, WEST
                            
                            self.moves = [MoveAction(NORTH), MoveAction(EAST), MoveAction(SOUTH), MoveAction(WEST)]
                            self.x = 0
                            
                        def handle_turn(self, world_map, avatar_state):
                            move = self.moves[self.x]
                            self.x += 1
                            return move
                 '''
        runner = AvatarRunner()

        directions = [NORTH, EAST, SOUTH, WEST]
        for direction in directions:
            response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
            self.assertEqual(response['action'], {'action_type': 'move', 'options': {'direction': direction}})

    def test_update_code_flag_simple(self):
        avatar1 = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH
                            
                            return MoveAction(NORTH)
                  '''
        avatar2 = '''class Avatar(object):
                                def handle_turn(self, world_map, avatar_state):
                                    from simulation.action import MoveAction
                                    from simulation.direction import SOUTH

                                    return MoveAction(SOUTH)
                  '''

        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertTrue(response['avatar_updated'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertFalse(response['avatar_updated'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)
        self.assertTrue(response['avatar_updated'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)
        self.assertFalse(response['avatar_updated'])

    def test_update_code_flag_with_syntax_errors(self):
        avatar = '''class Avatar(object:
                        pass
                 '''
        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertTrue(response['avatar_updated'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertFalse(response['avatar_updated'])

    def test_invalid_action_exception(self):
        avatar = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH
                            
                  '''
        runner = AvatarRunner()
        runner._update_avatar(src_code=avatar)
        with self.assertRaises(InvalidActionException):
            runner.decide_action(world_map={}, avatar_state={})

    def test_updated_successful(self):
        avatar_ok = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH
                            
                            return MoveAction(NORTH)

                    '''

        avatar_syntax_error = '''class Avatar(object):
                                    def handle_turn(self, world_map, avatar_state):
                                        from simulation.action import MoveAction
                                        from simulation.direction import NORTH
                                        
                                        return MoveAction(NORTH

                              '''

        avatar_bad_constructor = '''class Avatar(object):
                                            def __init__(self):
                                                return 1 + 'foo'
                                            def handle_turn(self, world_map, avatar_state):
                                                from simulation.action import MoveAction
                                                from simulation.direction import NORTH

                                                return MoveAction(NORTH)
                                  '''

        runner = AvatarRunner()
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar_ok)
        self.assertTrue(runner.update_successful)
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar_syntax_error)
        self.assertFalse(runner.update_successful)
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar_bad_constructor)
        self.assertFalse(runner.update_successful)
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar_ok)
        self.assertTrue(runner.update_successful)

    def test_runtime_error_contains_only_user_traceback(self):
        avatar = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH
                            
                            1 + 'foo'

                            return MoveAction(NORTH)
                 '''
        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertFalse('/usr/src/app/' in response['log'])

    def test_syntax_error_contains_only_user_traceback(self):
        avatar = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH

                            return MoveAction(NORTH))))
                            
                 '''
        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertFalse('/usr/src/app/' in response['log'])

    def test_invalid_action_exception_contains_only_user_traceback(self):
        avatar1 = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH

                            return None
                            
                 '''
        avatar2 = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH

                            return 1
                            
                 '''
        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertFalse('/usr/src/app/' in response['log'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)
        self.assertFalse('/usr/src/app/' in response['log'])
