from __future__ import absolute_import

import logging
from simulation.action import MoveAction, WaitAction
from simulation.avatar.avatar_manager import AvatarManager
from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.direction import NORTH, EAST, SOUTH, WEST

LOGGER = logging.getLogger(__name__)


class DummyAvatar(AvatarWrapper):
    def __init__(self, player_id=1, initial_location=(0, 0)):
        # TODO: extract avatar state and state-altering methods into a new class.
        #       The new class is to be shared between DummyAvatarRunner and AvatarRunner
        super(DummyAvatar, self).__init__(
            player_id, initial_location, avatar_appearance=None
        )
        self.times_died = 0
        self.attack_strength = 1
        self.effects = set()
        self.resistance = 0

    def decide_action(self, worker_data):
        raise NotImplementedError()

    def next_turn(self, world_map=None, avatar_state=None):
        raise NotImplementedError()

    def add_event(self, event):
        self.events.append(event)

    def die(self, respawn_loc):
        self.location = respawn_loc
        self.times_died += 1

    def fetch_data(self, state_view):
        return {"action": "", "log": "Testing", "avatar_updated": False}

    def damage(self, amount):
        self.health -= amount
        return amount


class LiveDummy(DummyAvatar):
    """
    An avatar that still has a fully functioning worker.
    """

    def __init__(self, player_id=1, initial_location=(0, 0)):
        super(LiveDummy, self).__init__(player_id, initial_location)

    def decide_action(self, worker_data):
        self._action = self.next_turn()
        return True


class DeadDummy(DummyAvatar):
    """
    An avatar whose worker is no longer responding or returning an invalid action.
    """

    def __init__(self, player_id=1, initial_location=(0, 0)):
        super(DeadDummy, self).__init__(player_id, initial_location)

    def decide_action(self, worker_data):
        self._action = self.next_turn()
        return False

    def next_turn(self, world_map=None, avatar_state=None):
        return WaitAction(self)


class WaitDummy(LiveDummy):
    """
    Avatar that always waits.
    """

    def next_turn(self, world_map=None, avatar_state=None):
        return WaitAction(self)


class MoveDummy(LiveDummy):
    """
    Avatar that always moves in one direction.
    """

    def __init__(self, player_id, initial_location, direction):
        super(MoveDummy, self).__init__(player_id, initial_location)
        self._direction = direction

    def next_turn(self, world_map=None, avatar_state=None):
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

    def add_avatar(self, player_id, location=(0, 0)):
        try:
            dummy = self.dummy_list.pop(0)
        except IndexError:
            dummy = WaitDummy
        self.avatars_by_id[player_id] = dummy(player_id, location)
        return self.avatars_by_id[player_id]

    def add_avatar_directly(self, avatar):
        self.avatars_by_id[avatar.player_id] = avatar

    def get_player_id_to_serialized_action(self):
        for dummy in self.avatars_by_id.values():
            dummy.decide_action(None)

        return {
            player_id: self.avatars_by_id[player_id]._action
            for player_id in self.avatars_by_id
        }
