import logging
import time
from threading import Thread
from Queue import Queue

from simulation.action import PRIORITIES, MoveAction

LOGGER = logging.getLogger(__name__)


class TurnManager(Thread):
    """
    Game loop
    """
    daemon = True

    def __init__(self, game_state, end_turn_callback):
        self.game_state = game_state
        self.end_turn_callback = end_turn_callback
        super(TurnManager, self).__init__()

    def run_turn(self):
        raise NotImplementedError("Abstract method.")

    def run(self):
        while True:

            self.run_turn()

            self.game_state.end_of_turn()

            self.end_turn_callback()

            time.sleep(0.5)


class SequentialTurnManager(TurnManager):
    def run_turn(self):
        '''
        Get and apply each avatar's action in turn.
        '''
        for avatar in self.game_state.avatar_manager.active_avatars:
            state_view = self.game_state.view(avatar)
            action = avatar.decide_action(state_view)

            with self.game_state:
                action.process(self.game_state)


class ConcurrentTurnManager(TurnManager):
    def run_turn(self):
        '''
        Concurrently get the intended actions from all avatars and apply them
        in order of priority.
        '''
        threads = [DecisionThread(avatar, self.game_state.view(avatar))
                   for avatar in self.game_state.avatar_manager.active_avatars]

        [thread.start() for thread in threads]

        actions = ActionRegistry()
        for thread in threads:
            actions.add(thread.result())

        for action in actions.sorted_by_type:
            with self.game_state:
                action.process(self.game_state, actions)


class DecisionThread(Thread):
    '''
    Thread wrapper to get an avatar's decided action.
    '''
    def __init__(self, avatar, state_view):
        self._queue = Queue()
        super(DecisionThread, self).__init__(
            target=self.wrapper,
            args=(avatar, state_view)
        )

    def wrapper(self, avatar, state_view):
        self._queue.put(avatar.decide_action(state_view))

    def result(self):
        return self._queue.get()


class ActionRegistry(object):
    '''
    Class to keep track of the actions that avatars intend to perform
    in a concurrent turn.
    '''
    def __init__(self):
        self.clear()

    def add(self, action):
        self._actions_by_avatar[action.avatar_id] = action
        self._by_target(action.target).append(action)

    def clear(self):
        self._actions_by_avatar = {}
        self._actions_by_target = {}

    def by_avatar(self, avatar_id):
        return self._actions_by_avatar.setdefault(avatar_id, None)

    def avatar_moving(self, avatar_id):
        return isinstance(self.by_avatar(avatar_id), MoveAction)

    def _by_target(self, target):
        return self._actions_by_target.setdefault(target, [])

    def by_target(self, target):
        return (action for action in self._by_target(target))

    def moves_to(self, target):
        return (a for a in self.by_target(target) if isinstance(a, MoveAction))

    def num_moves_to(self, target):
        return sum(1 for move in self.moves_to(target))

    @property
    def sorted_by_type(self):
        action_list = self._actions_by_avatar.values()
        action_list.sort(key=lambda a: PRIORITIES[type(a)])
        return (action for action in action_list)


TURN_MANAGERS = {
    'sequential': SequentialTurnManager,
    'concurrent': ConcurrentTurnManager,
}
