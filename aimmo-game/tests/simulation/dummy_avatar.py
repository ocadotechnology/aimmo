from __future__ import absolute_import

import itertools

from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.avatar.avatar_manager import AvatarManager
from simulation.action import MoveAction, WaitAction
from simulation.direction import NORTH, EAST, SOUTH, WEST


class DummyAvatar(AvatarWrapper):
    def __init__(self, user_id):
        super(DummyAvatar, self).__init__(user_id, None, None)

    def decide_action(self, state_view):
        return self.handle_turn(state_view)

    def handle_turn(self, state_view):
        raise NotImplementedError()

    def die(self, respawn_loc):
        self.location = respawn_loc
        self.times_died += 1

    def serialise(self):
        return 'Dummy'


class WaitDummy(DummyAvatar):
    '''
    Avatar that always waits.
    '''
    def handle_turn(self, state_view):
        return WaitAction(self.user_id, self.location)


class MoveDummy(DummyAvatar):
    '''
    Avatar that always moves in one direction.
    '''
    def __init__(self, user_id, direction):
        super(MoveDummy, self).__init__(user_id)
        self._direction = direction

    def handle_turn(self, state_view):
        return MoveAction(self.user_id, self.location, self._direction.dict)


class MoveNorthDummy(MoveDummy):
    def __init__(self, user_id):
        super(MoveNorthDummy, self).__init__(user_id, NORTH)


class MoveEastDummy(MoveDummy):
    def __init__(self, user_id):
        super(MoveEastDummy, self).__init__(user_id, EAST)


class MoveSouthDummy(MoveDummy):
    def __init__(self, user_id):
        super(MoveSouthDummy, self).__init__(user_id, SOUTH)


class MoveWestDummy(MoveDummy):
    def __init__(self, user_id):
        super(MoveWestDummy, self).__init__(user_id, WEST)


class DummyAvatarManager(AvatarManager):
    def __init__(self, dummy_list=[]):
        super(DummyAvatarManager, self).__init__()
        self._dummy_list = dummy_list

    def add_avatar(self, avatar_id, worker_url):
        try:
            dummy = self._dummy_list.pop(0)
        except IndexError:
            dummy = DummyAvatar
        self._avatars_by_id[avatar_id] = dummy(avatar_id)
        return self._avatars_by_id[avatar_id]

    def add_avatar_directly(self, avatar):
        self._avatars_by_id[avatar.user_id] = avatar
