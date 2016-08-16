from __future__ import absolute_import
from simulation.location import Location


class DummyAvatarRunner(object):
    def __init__(self, initial_location, player_id):
        # TODO: extract avatar state and state-altering methods into a new class.
        #       The new class is to be shared between DummyAvatarRunner and AvatarRunner
        self.health = 5
        self.score = 0
        self.location = initial_location
        self.player_id = player_id
        self.events = []
        self.times_died = 0
        self.attack_strength = 1

    def take_turn(self, game_state, turn_state):
        self.location += Location(1, 0)

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


class EmptyAvatarManager(object):
    def __init__(self):
        self.avatarsById = {}

    def remove_avatar(self, id):
        del self.avatarsById[id]

    def add_avatar(self, id, url, location):
        self.avatarsById[id] = DummyAvatarRunner(location, id)

    def add_avatar_object(self, avatar):
        self.avatarsById[avatar.player_id] = avatar

    @property
    def active_avatars(self):
        return self.avatarsById.values()
