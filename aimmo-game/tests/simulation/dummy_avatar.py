from __future__ import absolute_import

from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.avatar.avatar_manager import AvatarManager
from simulation.action import MoveAction
from simulation import direction


class DummyAvatarRunner(AvatarWrapper):
    def __init__(self, initial_location, player_id):
        # TODO: extract avatar state and state-altering methods into a new class.
        #       The new class is to be shared between DummyAvatarRunner and AvatarRunner
        self.player_id = player_id
        self.location = initial_location
        self.health = 5
        self.score = 0
        self.events = []
        self.times_died = 0
        self._action = None

    def decide_action(self, state_view):
        self._action = self.handle_turn(state_view)
        return True

    def handle_turn(self, state_view):
        next_action = MoveAction(self, direction.EAST.dict)
        return next_action

    def add_event(self, event):
        self.events.append(event)

    def die(self, respawn_loc):
        self.location = respawn_loc
        self.times_died += 1

    def serialise(self):
        return 'Dummy'


class DummyAvatarManager(AvatarManager):
    def __init__(self, avatars):
        self.avatars_by_id = {a.player_id: a for a in avatars}

    def add_avatar_directly(self, avatar):
        self.avatars_by_id[avatar.player_id] = avatar
