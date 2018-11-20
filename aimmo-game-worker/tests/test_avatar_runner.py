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
        avatar = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            assert False'''

        runner = AvatarRunner(avatar=avatar, auto_update=False)
        action = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code='')['action']
        self.assertEqual(action, {'action_type': 'wait'})

    def test_runner_updates_code_on_change(self):
        avatar1 = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            
                            return MoveAction(direction.EAST)
                  '''
        avatar2 = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            
                            return MoveAction(direction.WEST)
                  '''

        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertEqual(response['action'], {'action_type': 'move', 'options': {'direction': EAST}})

        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)

        self.assertEqual(response['action'], {'action_type': 'move', 'options': {'direction': WEST}})

    def test_update_code_flag_simple(self):
        avatar1 = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            
                            return MoveAction(direction.NORTH)
                  '''
        avatar2 = '''class Avatar:
                                def handle_turn(self, world_map, avatar_state):

                                    return MoveAction(direction.SOUTH)
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
        avatar = '''class Avatar
                        pass
                 '''
        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertTrue(response['avatar_updated'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertFalse(response['avatar_updated'])

    def test_invalid_action_exception(self):
        avatar = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                        
                            new_dir = random.choice(direction.ALL_DIRECTIONS)
                  '''
        runner = AvatarRunner()
        runner._update_avatar(src_code=avatar)
        with self.assertRaises(InvalidActionException):
            runner.decide_action(world_map={}, avatar_state={})

    def test_does_not_update_with_imports(self):
        avatar = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            import os
                            return MoveAction(random.choice(direction.ALL_DIRECTIONS))
                  '''
        runner = AvatarRunner()
        runner._update_avatar(src_code=avatar)
        with self.assertRaises(ImportError):
            runner.decide_action(world_map={}, avatar_state={})

    def test_updated_successful(self):
        avatar_ok = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            
                            return MoveAction(direction.NORTH)

                    '''

        avatar_syntax_error = '''class Avatar:
                                    def handle_turn(self, world_map, avatar_state):
                                        
                                        return MoveAction(direction.NORTH

                              '''

        avatar_bad_constructor = '''class Avatar:
                                            def __init__(self):
                                                return 1 + 'foo'
                                            def handle_turn(self, world_map, avatar_state):

                                                return MoveAction(direction.NORTH)
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

    def test_updates_with_for_loop(self):
        avatar = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            x = 0
                            for x in range(5):
                                x = x + 1
                                print(x)
                                
                            return MoveAction(random.choice(direction.ALL_DIRECTIONS))
                  '''
        runner = AvatarRunner()
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertTrue(runner.update_successful)

    def test_updates_with_inplace_operator(self):
        avatar = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            x = 0
                            x += 2
                                
                            return MoveAction(random.choice(direction.ALL_DIRECTIONS))
                  '''
        runner = AvatarRunner()
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertTrue(runner.update_successful)

    def test_runtime_error_contains_only_user_traceback(self):
        avatar = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):
                            
                            1 + 'foo'

                            return MoveAction(direction.NORTH)
                 '''
        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertFalse('/usr/src/app/' in response['log'])

    def test_syntax_error_contains_only_user_traceback(self):
        avatar = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):

                            return MoveAction(direction.NORTH))))
                            
                 '''
        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertFalse('/usr/src/app/' in response['log'])

    def test_invalid_action_exception_contains_only_user_traceback(self):
        avatar1 = '''class Avatar
                        def handle_turn(self, world_map, avatar_state):

                            return None
                            
                 '''
        avatar2 = '''class Avatar:
                        def handle_turn(self, world_map, avatar_state):

                            return 1
                            
                 '''
        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertFalse('/usr/src/app/' in response['log'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)
        self.assertFalse('/usr/src/app/' in response['log'])
