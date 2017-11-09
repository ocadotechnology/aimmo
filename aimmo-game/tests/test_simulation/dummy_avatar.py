from __future__ import absolute_import

from simulation.action import MoveAction, WaitAction
from simulation.avatar.avatar_manager import AvatarManager
from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.direction import NORTH, EAST, SOUTH, WEST


class DummyAvatar(AvatarWrapper):
    def __init__(self, player_id=1, initial_location=(0, 0)):
        # TODO: extract avatar state and state-altering methods into a new class.
        #       The new class is to be shared between DummyAvatarRunner and AvatarRunner
        super(DummyAvatar, self).__init__(player_id, initial_location, None, None)
        self.times_died = 0
        self.attack_strength = 1
        self.effects = set()
        self.resistance = 0

    def decide_action(self, state_view):
        self._action = self.handle_turn(state_view)
        return True

    def handle_turn(self, state_view):
        raise NotImplementedError()

    def add_event(self, event):
        self.events.append(event)

    def die(self, respawn_loc):
        self.location = respawn_loc
        self.times_died += 1

    def serialise(self):
        return 'Dummy'

    def damage(self, amount):
        self.health -= amount
        return amount


class WaitDummy(DummyAvatar):
    """
    Avatar that always waits.
    """
    def handle_turn(self, state_view):
        return WaitAction(self)


class MoveDummy(DummyAvatar):
    """
    Avatar that always moves in one direction.
    """
    def __init__(self, player_id, initial_location, direction):
        super(MoveDummy, self).__init__(player_id, initial_location)
        self._direction = direction

    def handle_turn(self, state_view):
        return MoveAction(self, self._direction.dict)


class MoveNorthDummy(MoveDummy):
    def __init__(self, player_id, initial_location):
        super(MoveNorthDummy, self).__init__(player_id, initial_location, NORTH)


class MoveEastDummy(MoveDummy):
    def __init__(self, player_id, initial_location):
        super(MoveEastDummy, self).__init__(player_id, initial_location, EAST)


class MoveSouthDummy(MoveDummy):
    def __init__(self, player_id, initial_location):
        super(MoveSouthDummy, self).__init__(player_id, initial_location, SOUTH)


class MoveWestDummy(MoveDummy):
    def __init__(self, player_id, initial_location):
        super(MoveWestDummy, self).__init__(player_id, initial_location, WEST)


class DummyAvatarManager(AvatarManager):
    def __init__(self, dummy_list=None):
        super(DummyAvatarManager, self).__init__()
        if dummy_list is None:
            dummy_list = []
        self.dummy_list = dummy_list

    def add_avatar(self, player_id, worker_url, location):
        try:
            dummy = self.dummy_list.pop(0)
        except IndexError:
            dummy = WaitDummy
        self.avatars_by_id[player_id] = dummy(player_id, location)
        return self.avatars_by_id[player_id]

    def add_avatar_directly(self, avatar):
        self.avatars_by_id[avatar.player_id] = avatar
