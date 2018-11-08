from __future__ import print_function

import logging
import traceback
import sys
import imp

from six import StringIO

from simulation.action import WaitAction, Action, MoveAction
import simulation.direction as direction
from user_exceptions import InvalidActionException

from RestrictedPython import compile_restricted, compile_restricted_exec, utility_builtins, limited_builtins
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import safe_builtins, full_write_guard



LOGGER = logging.getLogger(__name__)

try:
    import __builtin__
except ImportError:
    raise ImportError
    # Python 3
    # import builtins as __builtin__


def print_text(*args, **kwargs):
    """My custom print() function."""
    # Adding new arguments to the print function signature
    # is probably a bad idea.
    # Instead consider testing if custom argument keywords
    # are present in kwargs
    __builtin__.print('My overridden print() function!')
    return __builtin__.print(*args, **kwargs)


def our_import(name, globals=None, locals=None, fromlist=None):
    # Fast path: see if the module has already been imported.
    try:
        return sys.modules[name]
    except KeyError:
        pass

    # If any of the following calls raises an exception,
    # there's a problem we can't handle -- let the caller handle it.

    fp, pathname, description = imp.find_module(name)

    try:
        return imp.load_module(name, fp, pathname, description)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()


_write_ = full_write_guard
_getattr_ = getattr
__metaclass__ = type
restricted_globals = dict(__builtins__=safe_builtins)
restricted_globals['_print_'] = print_text
restricted_globals['_import_'] = our_import
restricted_globals['_write_'] = _write_
restricted_globals['_getattr_'] = _getattr_
restricted_globals['__builtins__']['object'] = '<type "object">'
restricted_globals['object'] = '<type "object">'
restricted_globals['__metaclass__'] = __metaclass__
restricted_globals['__name__'] = "Avataaar"
restricted_globals['WaitAction'] = WaitAction
restricted_globals['MoveAction'] = MoveAction
restricted_globals['direction'] = direction
restricted_globals['random'] = utility_builtins['random']


class AvatarRunner(object):
    def __init__(self, avatar=None, auto_update=True):
        self.avatar = avatar
        self.auto_update = auto_update
        self.avatar_source_code = None
        self.update_successful = False

    def _avatar_src_changed(self, new_avatar_code):
        return new_avatar_code != self.avatar_source_code

    def _get_new_avatar(self, src_code):

        # src_code = src_code.encode('utf-8')

        # self.avatar_source_code = '''class Avatar:
        #                                 def handle_turn(self, world_state, avatar_state):
        #
        #                                     first_name = "Florian"
        #                                     last_name = "Aucomte"
        #                                     name = first_name + last_name
        #                                     print(name)
        #
        #                                     new_dir = random.choice(direction.ALL_DIRECTIONS)
        #                                     return MoveAction(new_dir)'''

        # self.avatar_source_code = '''class Avatar:
        #                                def handle_turn(self, world_state, avatar_state):
        #                                    print("Hello world")
        #                                    return MoveAction(direction.NORTH)'''

        self.avatar_source_code = src_code

        # LOGGER.info(src_code)

        # LOGGER.info(type(src_code))

        # self.avatar_source_code = 'a = 5\nb=10\nprint("Sum =", a+b)'

        # LOGGER.info(self.avatar_source_code)

        module_avatar = imp.new_module('avatar')  # Create a temporary module to execute the src_code in

        # LOGGER.info(globals())

        module_avatar.__dict__.update(restricted_globals)

        # LOGGER.info(module_avatar.__dict__)

        # LOGGER.info(type(object))
        # restricted_globals['__name__'] = 'avatar_runner'

        # LOGGER.info(restricted_globals)

        try:
            byte_code = compile_restricted(src_code, filename='<inline-code>', mode='exec')
            # byte_code = compile(self.avatar_source_code, filename='code', mode='exec')
            # LOGGER.info(type(byte_code))
            # LOGGER.info(byte_code)

            # LOGGER.info(safe_globals)
            # LOGGER.info(module_lel.__dict__)

            # module.__dict__.update(safe_globals)

            # exec byte_code in module_avatar.__dict__
            exec byte_code in restricted_globals
        except SyntaxError as e:
            pass

        # byte_code = compile_restricted(src_code, filename='<inline code>', mode='exec')
        # exec self.avatar_source_code in module_avatar.__dict__
        return module_avatar.Avatar()

    def _update_avatar(self, src_code):
        """
        We update the avatar object if any of the following are true:
        1. We don't have an avatar object yet, so self.avatar is None
        2. The new source code we have been given is different
        3. If the previous attempt to create an avatar object failed (i.e. _get_new_avatar threw an exception)
        The last condition is necessary because if _get_new_avatar fails the avatar object will not have
        been updated, meaning that self.avatar will actually be for the last correct code
        """
        should_update = (self.avatar is None or
                         self.auto_update and self._avatar_src_changed(src_code) or
                         not self.update_successful)

        LOGGER.info(self.avatar is None)
        LOGGER.info(self.auto_update)
        LOGGER.info(self._avatar_src_changed(src_code))
        LOGGER.info(not self.update_successful)

        if should_update:
            try:
                self.avatar = self._get_new_avatar(src_code)
            except Exception as e:
                self.update_successful = False
                raise e
            else:
                self.update_successful = True

    def process_avatar_turn(self, world_map, avatar_state, src_code):
        output_log = StringIO()
        avatar_updated = self._avatar_src_changed(src_code)

        try:
            sys.stdout = output_log
            sys.stderr = output_log
            self._update_avatar(src_code)
            action = self.decide_action(world_map, avatar_state)

        # When an InvalidActionException is raised, the traceback might not contain
        # reference to the user's code as it can still technically be correct. so we
        # handle this case explicitly to avoid printing out unwanted parts of the traceback
        except InvalidActionException as e:
            print(e)
            action = WaitAction().serialise()

        except Exception as e:
            user_traceback = self.get_only_user_traceback()
            for trace in user_traceback:
                print(trace)

            LOGGER.info("Code failed to run")
            LOGGER.info(e)
            action = WaitAction().serialise()

        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        logs = output_log.getvalue()
        return {'action': action, 'log': logs, 'avatar_updated': avatar_updated}

    def decide_action(self, world_map, avatar_state):
        action = self.avatar.handle_turn(world_map, avatar_state)
        if not isinstance(action, Action):
            raise InvalidActionException(action)
        return action.serialise()

    @staticmethod
    def get_only_user_traceback():
        """ If the traceback does not contain any reference to the user code, found by '<string>',
            then this method will just return the full traceback. """
        traceback_list = traceback.format_exc().split('\n')
        start_of_user_traceback = 0
        for i in range(len(traceback_list)):
            if '<string>' in traceback_list[i]:
                start_of_user_traceback = i
                break
        return traceback_list[start_of_user_traceback:]
