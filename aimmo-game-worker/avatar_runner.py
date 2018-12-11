from __future__ import print_function

import logging
import traceback
import sys
import imp
import inspect
import re

from io import StringIO
import contextlib

import simulation.action as avatar_action
import simulation.direction as direction
from print_collector import LogManager

from simulation.action import WaitAction, Action
from user_exceptions import InvalidActionException

from RestrictedPython import compile_restricted, utility_builtins
from RestrictedPython.Guards import safe_builtins, safer_getattr, guarded_setattr, full_write_guard
from RestrictedPython.PrintCollector import PrintCollector

LOGGER = logging.getLogger(__name__)


def add_actions_to_globals():
    action_classes = filter(lambda x: x[1].__module__ == "simulation.action", inspect.getmembers(avatar_action, inspect.isclass))

    for action_class in action_classes:
        restricted_globals[action_class[0]] = action_class[1]


_getattr_ = safer_getattr
_setattr_ = guarded_setattr
_write_ = full_write_guard
__metaclass__ = type

# Sets up restricted coding environment for the user
log_manager = LogManager()
restricted_globals = dict(__builtins__=safe_builtins)

restricted_globals['_getattr_'] = _getattr_
restricted_globals['_setattr_'] = _setattr_
restricted_globals['_getiter_'] = list
restricted_globals['_print_'] = log_manager.get_print_collector()
restricted_globals['_write_'] = _write_
restricted_globals['__metaclass__'] = __metaclass__
restricted_globals['__name__'] = "Avatar"

# Adds AI:MMO specific modules to the user's environment
add_actions_to_globals()
restricted_globals['direction'] = direction
restricted_globals['random'] = utility_builtins['random']

# Temporarily switches stdout and stderr to stringIO objects or variable
@contextlib.contextmanager
def capture_output(stdout=None, stderr=None):
    oldout = sys.stdout
    olderr = sys.stderr

    if stdout is None:
        stdout = StringIO()
    if stderr is None:
        stderr = StringIO()
    sys.stdout = stdout
    sys.stderr = stderr
    yield stdout, stderr

    sys.stdout = oldout
    sys.stderr = olderr



class AvatarRunner(object):
    def __init__(self, avatar=None, auto_update=True):
        self.avatar = avatar
        self.auto_update = auto_update
        self.avatar_source_code = None
        self.update_successful = False

    def _avatar_src_changed(self, new_avatar_code):
        return new_avatar_code != self.avatar_source_code

    def _get_new_avatar(self, src_code):
        self.avatar_source_code = src_code
        module = imp.new_module('avatar')  # Create a temporary module to execute the src_code in
        module.__dict__.update(restricted_globals)

        try:
            byte_code = compile_restricted(src_code, filename='<inline-code>', mode='exec')
            exec(byte_code, restricted_globals)
        except SyntaxWarning as w:
            pass

        module.__dict__['Avatar'] = restricted_globals['Avatar']
        return module.Avatar()

    def _update_avatar(self, src_code):
        """
        We update the avatar object if any of the following are true:
        1. We don't have an avatar object yet, so self.avatar is None
        2. The new source code we have been given is different
        3. If the previous attempt to create an avatar object failed (i.e. _get_new_avatar threw an exception)
        The last condition is necessary because if _get_new_avatar fails the avatar object will not have
        been updated, meaning that self.avatar will actually be for the last correct code
        """

        if self._should_update(src_code):
            try:
                self.avatar = self._get_new_avatar(src_code)
            except Exception as e:
                self.update_successful = False
                raise e
            else:
                self.update_successful = True

    def _should_update(self, src_code):
        return (self.avatar is None or self.auto_update and self._avatar_src_changed(src_code) or
                not self.update_successful)

    def process_avatar_turn(self, world_map, avatar_state, src_code):
        avatar_updated = self._avatar_src_changed(src_code)

        with capture_output() as output:
            try:
                self._update_avatar(src_code)
                action = self.decide_action(world_map, avatar_state)
                self.print_logs()

            # This needs to be handled explicitly as the users code and still be technically correct here.
            except InvalidActionException as e:
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

        stdout, stderr = output
        output_log = stdout.getvalue()
        if not stderr.getvalue() == '':
            LOGGER.info(stderr.getvalue())

        return {'action': action, 'log': output_log, 'avatar_updated': avatar_updated}

    def decide_action(self, world_map, avatar_state):
        try:
            action = self.avatar.handle_turn(world_map, avatar_state)
            if not isinstance(action, Action):
                raise InvalidActionException(action)
            return action.serialise()
        except TypeError as e:
                print(e)
                raise InvalidActionException(None)

    @staticmethod
    def get_only_user_traceback():
        """ If the traceback does not contain any reference to the user code, found by '<string>',
            then this method will just return the full traceback. """
        traceback_list = traceback.format_exc().split('\n')
        start_of_user_traceback = 0
        for i in range(len(traceback_list)):
            if '<inline-code>' in traceback_list[i]:
                start_of_user_traceback = i
                break
        return traceback_list[start_of_user_traceback:]

    @staticmethod
    def print_logs():
        if not log_manager.is_empty():
            print(log_manager.get_logs(), end='')
            log_manager.clear_logs()
