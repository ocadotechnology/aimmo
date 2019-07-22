from unittest import TestCase

import mock
from avatar_runner import AvatarRunner
from code_updater import CodeUpdater
from user_exceptions import InvalidActionException

NORTH = {"x": 0, "y": 1}
SOUTH = {"x": 0, "y": -1}
EAST = {"x": 1, "y": 0}
WEST = {"x": -1, "y": 0}


class TestAvatarRunner(TestCase):
    def test_runner_does_not_crash_on_code_errors(self):
        avatar = """
def next_turn(world_map, avatar_state):
    assert False
                """

        runner = AvatarRunner(code_updater=CodeUpdater())
        action = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )["action"]
        self.assertEqual({"action_type": "wait"}, action)

    def test_runner_gives_wait_action_on_compile_errors(self):
        avatar = """
def next_turn(world_map, avatar_state):
    return MoveAction(direction.WEST)))))
                """

        runner = AvatarRunner(code_updater=CodeUpdater())
        action = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )["action"]
        self.assertEqual({"action_type": "wait"}, action)

    def test_runner_updates_code_on_change(self):
        avatar1 = """
def next_turn(world_map, avatar_state):
    return MoveAction(direction.EAST)
                  """
        avatar2 = """
def next_turn(world_map, avatar_state):
    return MoveAction(direction.WEST)
                  """

        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar1
        )
        self.assertEqual(
            {"action_type": "move", "options": {"direction": EAST}}, response["action"]
        )

        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar2
        )

        self.assertEqual(
            {"action_type": "move", "options": {"direction": WEST}}, response["action"]
        )

    def test_update_code_flag_simple(self):
        avatar1 = """
def next_turn(world_map, avatar_state):
    return MoveAction(direction.NORTH)
                  """
        avatar2 = """
def next_turn(world_map, avatar_state):
    return MoveAction(direction.SOUTH)
                  """

        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar1
        )
        self.assertTrue(response["avatar_updated"])
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar1
        )
        self.assertFalse(response["avatar_updated"])
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar2
        )
        self.assertTrue(response["avatar_updated"])
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar2
        )
        self.assertFalse(response["avatar_updated"])

    def test_update_code_flag_with_syntax_errors(self):
        avatar = """
class Avatar
    pass
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertTrue(response["avatar_updated"])
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertFalse(response["avatar_updated"])

    def test_invalid_action_exception(self):
        avatar = """
def next_turn(world_map, avatar_state):
    new_dir = random.choice(direction.ALL_DIRECTIONS)
                  """
        runner = AvatarRunner(code_updater=CodeUpdater())
        runner.avatar, _ = runner.code_updater.update_avatar(src_code=avatar)
        with self.assertRaises(InvalidActionException):
            runner.decide_action(world_map={}, avatar_state={})

    def test_does_not_update_with_imports(self):
        avatar = """
def next_turn(world_map, avatar_state):
    import os
    return MoveAction(random.choice(direction.ALL_DIRECTIONS))
                  """
        runner = AvatarRunner(code_updater=CodeUpdater())
        runner.avatar, _ = runner.code_updater.update_avatar(src_code=avatar)
        with self.assertRaises(ImportError):
            runner.decide_action(world_map={}, avatar_state={})

    def test_updated_successful(self):
        avatar_ok = """
def next_turn(world_map, avatar_state):
    return MoveAction(direction.NORTH)
                    """

        avatar_syntax_error = """
def next_turn(world_map, avatar_state):
    return MoveAction(direction.NORTH
                              """

        runner = AvatarRunner(code_updater=CodeUpdater())
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar_ok)
        self.assertTrue(runner.code_updater.update_successful)
        runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar_syntax_error
        )
        self.assertFalse(runner.code_updater.update_successful)

    def test_updates_with_for_loop(self):
        avatar = """
def next_turn(world_map, avatar_state):
    x = 0
    for x in range(5):
        x = x + 1
        print(x)
        
    return MoveAction(random.choice(direction.ALL_DIRECTIONS))
                  """
        runner = AvatarRunner(code_updater=CodeUpdater())
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertTrue(runner.code_updater.update_successful)

    def test_updates_with_inplace_operator(self):
        avatar = """
def next_turn(world_map, avatar_state):
    x = 0
    x += 2
        
    return MoveAction(random.choice(direction.ALL_DIRECTIONS))
                  """
        runner = AvatarRunner(code_updater=CodeUpdater())
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertTrue(runner.code_updater.update_successful)

    def test_runtime_error_contains_only_user_traceback(self):
        avatar = """
def next_turn(world_map, avatar_state):
    1 + 'foo'

    return MoveAction(direction.NORTH)
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertFalse("/usr/src/app/" in response["log"])

    def test_syntax_error_contains_only_user_traceback(self):
        avatar = """
def next_turn(world_map, avatar_state):
    return MoveAction(direction.NORTH))))
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertFalse("/usr/src/app/" in response["log"])

    def test_invalid_action_exception_contains_only_user_traceback(self):
        avatar1 = """
def next_turn(world_map, avatar_state):
    return None
                 """
        avatar2 = """
def next_turn(world_map, avatar_state):
    return 1
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar1
        )
        self.assertFalse("/usr/src/app/" in response["log"])
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar2
        )
        self.assertFalse("/usr/src/app/" in response["log"])

    def test_print_collector_outputs_logs(self):
        avatar = """
def next_turn(world_map, avatar_state):
    print('I AM A PRINT STATEMENT')
    return MoveAction(direction.NORTH)
                 """

        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertTrue("I AM A PRINT STATEMENT" in response["log"])

    def test_print_collector_outputs_multiple_prints(self):
        avatar = """
def next_turn(world_map, avatar_state):
    print('I AM A PRINT STATEMENT')
    print('I AM ALSO A PRINT STATEMENT')
    return MoveAction(direction.NORTH)
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertTrue("I AM A PRINT STATEMENT" in response["log"])
        self.assertTrue("I AM ALSO A PRINT STATEMENT" in response["log"])

    def test_print_collector_outputs_prints_from_different_scopes(self):
        avatar = """
def next_turn(world_map, avatar_state):
    print('I AM NOT A NESTED PRINT')
    foo()
    return MoveAction(direction.NORTH)
                                                
def foo():
    print('I AM A NESTED PRINT')
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertTrue("I AM NOT A NESTED PRINT" in response["log"])
        self.assertTrue("I AM A NESTED PRINT" in response["log"])

    def test_print_collector_prints_output_and_runtime_error_if_exists(self):
        avatar = """
def next_turn(world_map, avatar_state):
    print('THIS CODE IS BROKEN')
    return None
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertTrue("THIS CODE IS BROKEN" in response["log"])
        self.assertTrue('"None" is not a valid action object.' in response["log"])

    def test_syntax_errors_are_detected_correctly(self):
        avatar = """
def next_turn(world_map, avatar_state):
    print('THIS CODE IS BROKEN')
    return MoveAction(direction.NORTH))))))))
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertFalse(runner.code_updater.update_successful)
        runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
        self.assertFalse(runner.code_updater.update_successful)

    def test_syntax_warning_not_shown_to_user(self):
        avatar = """
def next_turn(world_map, avatar_state):
    print('I AM A PRINT')
    return MoveAction(direction.NORTH)
                 """
        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar
        )
        self.assertFalse("SyntaxWarning" in response["log"])

    def test_safe_getitem(self):
        avatar1 = """
def next_turn(world_map, avatar_state):
    mylist = [i for i in range(10)]
    mylist[0]
    mylist[4]
    return MoveAction(direction.NORTH)
                 """

        avatar2 = """
def next_turn(world_map, avatar_state):
    mylist = {i:i for i in range(10)}
    mylist[0]
    mylist[4]
    return MoveAction(direction.NORTH)
                 """

        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar1
        )
        self.assertTrue("Error" not in response["log"])
        self.assertEqual(
            {"action_type": "move", "options": {"direction": NORTH}}, response["action"]
        )

        runner = AvatarRunner(code_updater=CodeUpdater())
        response = runner.process_avatar_turn(
            world_map={}, avatar_state={}, src_code=avatar2
        )
        self.assertTrue("Error" not in response["log"])
        self.assertEqual(
            {"action_type": "move", "options": {"direction": NORTH}}, response["action"]
        )
