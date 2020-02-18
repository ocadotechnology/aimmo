from __future__ import print_function

import contextlib
import traceback

import logging
import sys
from io import StringIO

from print_collector import LogManager
from simulation.action import Action, WaitAction
from user_exceptions import InvalidActionException

LOGGER = logging.getLogger(__name__)
log_manager = LogManager()


@contextlib.contextmanager
def capture_output(stdout=None, stderr=None):
    """Temporarily switches stdout and stderr to stringIO objects or variable."""
    old_out = sys.stdout
    old_err = sys.stderr

    if stdout is None:
        stdout = StringIO()
    if stderr is None:
        stderr = StringIO()
    sys.stdout = stdout
    sys.stderr = stderr
    yield stdout, stderr

    sys.stdout = old_out
    sys.stderr = old_err


class AvatarRunner(object):
    def __init__(self, avatar=None, auto_update=True, code_updater=None):
        self.avatar = avatar
        self.auto_update = auto_update
        self.code_updater = code_updater
        self.code_updater.globals["_print_"] = log_manager.get_print_collector()

    def process_avatar_turn(self, world_map, avatar_state, src_code):
        avatar_updated = False
        with capture_output() as output:
            if self.code_updater.should_update(self.avatar, self.auto_update, src_code):
                self.avatar, avatar_updated = self.code_updater.update_avatar(src_code)

            if self.avatar:
                action = self.run_users_code(world_map, avatar_state, src_code)
            else:
                action = WaitAction().serialise()

        stdout, stderr = output
        output_log = stdout.getvalue()
        if not stderr.getvalue() == "":
            LOGGER.info(stderr.getvalue())

        return {"action": action, "log": output_log, "avatar_updated": avatar_updated}

    def run_users_code(self, world_map, avatar_state, src_code):
        try:
            action = self.decide_action(world_map, avatar_state)
            self.print_logs()

        except InvalidActionException as e:
            self.print_logs()
            print(e)
            action = WaitAction().serialise()
        except AttributeError as e:
            self.print_logs()
            print(e)
            action = WaitAction().serialise()
        except Exception as e:
            self.print_logs()
            user_traceback = self.get_only_user_traceback()
            for trace in user_traceback:
                print(trace)

            LOGGER.info("Code failed to run")
            LOGGER.info(e)
            action = WaitAction().serialise()

        return action

    def decide_action(self, world_map, avatar_state):
        try:
            action = self.avatar.next_turn(world_map, avatar_state)
            if not isinstance(action, Action):
                raise InvalidActionException(action)

            return action.serialise()
        except TypeError as e:
            print(e)
            return WaitAction().serialise()

    @staticmethod
    def get_only_user_traceback():
        """ If the traceback does not contain any reference to the user code, found by '<inline-code>',
            then this method will just return the full traceback. """
        traceback_list = traceback.format_exc().split("\n")
        start_of_user_traceback = 0
        for i in range(len(traceback_list)):
            if "<inline-code>" in traceback_list[i]:
                start_of_user_traceback = i
                break
        return traceback_list[start_of_user_traceback:]

    @staticmethod
    def print_logs():
        """ Prints out stdout from the users code. """
        if not log_manager.is_empty():
            print(log_manager.get_logs(), end="")
            log_manager.clear_logs()
