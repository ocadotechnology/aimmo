from __future__ import print_function

from simulation.action import WaitAction, MoveAction
import simulation.direction as direction

from RestrictedPython import utility_builtins
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import safe_builtins, full_write_guard

try:
    import __builtin__
except ImportError:
    raise ImportError
    # Python 3
    # import builtins as __builtin__


def print_text(*args, **kwargs):
    return __builtin__.print(*args, **kwargs)


_write_ = full_write_guard
_getattr_ = getattr
__metaclass__ = type
restricted_globals = dict(__builtins__=safe_builtins)
__dict__['_print_'] = print_text
__dict__['_write_'] = _write_
__dict__['_getattr_'] = _getattr_
__dict__['__metaclass__'] = __metaclass__
__dict__['WaitAction'] = WaitAction
__dict__['MoveAction'] = MoveAction
__dict__['direction'] = direction
__dict__['random'] = utility_builtins['random']

__name__ = 'avatar'
