from __future__ import print_function

import imp
import inspect

from RestrictedPython import compile_restricted, utility_builtins
from RestrictedPython.Guards import (
    full_write_guard,
    guarded_setattr,
    safe_builtins,
    safer_getattr,
)

from simulation import action as avatar_action
from simulation import direction as direction


def add_actions_to_globals():
    action_classes = filter(
        lambda x: x[1].__module__ == "simulation.action",
        inspect.getmembers(avatar_action, inspect.isclass),
    )

    for action_class in action_classes:
        restricted_globals[action_class[0]] = action_class[1]


def safe_getitem(l, idx):
    return l[idx]


_getattr_ = safer_getattr
_setattr_ = guarded_setattr
_write_ = full_write_guard
__metaclass__ = type

restricted_globals = dict(__builtins__=safe_builtins)

restricted_globals["_getattr_"] = _getattr_
restricted_globals["_setattr_"] = _setattr_
restricted_globals["_getiter_"] = list
restricted_globals["_write_"] = _write_
restricted_globals["__metaclass__"] = __metaclass__
restricted_globals["__name__"] = "Avatar"
restricted_globals["_getitem_"] = safe_getitem


# Adds Kurono specific modules to the user's environment
add_actions_to_globals()
restricted_globals["direction"] = direction
restricted_globals["random"] = utility_builtins["random"]


class CodeUpdater:
    def __init__(self):
        self.avatar_source_code = None
        self.update_successful = False
        self.globals = restricted_globals

    def update_avatar(self, src_code):
        """
        We update the avatar object if any of the following are true:
        1. We don't have an avatar object yet, so self.avatar is None
        2. The new source code we have been given is different
        3. If the previous attempt to create an avatar object failed (i.e. _get_new_avatar threw an exception)
        The last condition is necessary because if _get_new_avatar fails the avatar object will not have
        been updated, meaning that self.avatar will actually be for the last correct code
        """
        avatar = None
        new_code_recieved = self._avatar_src_changed(src_code)
        try:
            avatar = self._get_new_avatar(src_code)

            self.update_successful = True
        except SyntaxError as e:
            self.update_successful = False
            print(e)
        except Exception as e:
            self.update_successful = False
            raise e

        return (avatar, new_code_recieved)

    def _avatar_src_changed(self, new_avatar_code):
        return new_avatar_code != self.avatar_source_code

    def should_update(self, avatar, auto_update, src_code):
        return (
            avatar is None
            or auto_update
            and self._avatar_src_changed(src_code)
            or not self.update_successful
        )

    def _get_new_avatar(self, src_code):
        self.avatar_source_code = src_code
        module = imp.new_module(
            "avatar"
        )  # Create a temporary module to execute the src_code in

        try:
            byte_code = compile_restricted(
                src_code, filename="<inline-code>", mode="exec"
            )
            exec(byte_code, self.globals)
        except SyntaxWarning as w:
            pass

        module.__dict__.update(self.globals)
        return module
