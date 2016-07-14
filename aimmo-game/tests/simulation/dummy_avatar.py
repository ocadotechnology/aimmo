from __future__ import absolute_import
from simulation.action import MoveAction
from simulation import direction


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

    def handle_turn(self, state):
        next_action = MoveAction(direction.EAST)

        # Reset event log
        self.events = []

        return next_action

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
