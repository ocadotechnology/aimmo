from abc import ABCMeta, abstractmethod, abstractproperty
from functools import reduce
from logging import getLogger
from typing import TYPE_CHECKING

from simulation.pickups.conditions import TurnState, avatar_on_cell
from simulation.pickups.effects import (DamageBoostPickupEffect,
                                        InvulnerabilityPickupEffect)

if TYPE_CHECKING: 
    from simulation.world_map import WorldMap

LOGGER = getLogger(__name__)


DAMAGE_BOOST_DEFAULT = 5
HEALTH_RESTORE_DEFAULT = 3
HEALTH_RESTORE_MAX = 100
AVATAR_HEALTH_MAX = 100


class _Pickup(object):
    __metaclass__ = ABCMeta

    def __init__(self, cell):
        self.cell = cell
        self.conditions = []
        self.effects = []

    def __str__(self):
        return self.__class__.__name__

    def delete(self):
        self.cell.pickup = None

    def conditions_met(self, world_map: 'WorldMap'):
        """ Applies logical and on all conditions, returns True is all conditions are met. """
        turn_state = TurnState(world_map, self.cell)
        return all([condition(turn_state) for condition in self.conditions])

    @abstractmethod
    def apply(self, avatar=None, cell=None, region=None):
        raise NotImplementedError()

    @abstractmethod
    def serialise(self):
        raise NotImplementedError()


class HealthPickup(_Pickup):
    def __init__(self, cell, health_restored=HEALTH_RESTORE_DEFAULT):
        # Round the integer up to the nearest value (ceiling).
        health_restored = int(round(health_restored))
        # Check if the value provided is legal.
        if 0 < health_restored <= HEALTH_RESTORE_MAX:
            super(HealthPickup, self).__init__(cell)
            self.health_restored = health_restored
        else:
            raise ValueError("Health Restored has to be within 0-100 range!")

        self.conditions.append(avatar_on_cell)
        self.effects.append(self.give_health)
        self.effects.append(self.delete)

    def __repr__(self):
        return 'HealthPickup(health_restored={})'.format(self.health_restored)

    def serialise(self):
        return {
                'type': 'health',
                'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
                }
        }

    def give_health(self, avatar):
        avatar.health += self.health_restored

        # Make sure the health is capped at 100.
        if avatar.health > AVATAR_HEALTH_MAX:
            avatar.health = AVATAR_HEALTH_MAX
        
    def apply(self, avatar=None, cell=None, region=None):
        self.effects[0](avatar)
        self.effects[1]()


class InvulnerabilityPickup(_Pickup):
    def __init__(self, cell):
        super(InvulnerabilityPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)
        self.effects.append(InvulnerabilityPickupEffect)
        self.effects.append(self.delete)

    def apply(self, avatar=None, cell=None, region=None):
        self.effects[0](avatar)
        self.effects[1]()

    def __repr__(self):
        return 'InvulnerabilityPickup(damage_boost={})'.format(self.damage_boost)

    def serialise(self):
        return {
                'type': 'invulnerability',
                'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
                }
        }


class DamageBoostPickup(_Pickup):
    def __init__(self, cell, damage_boost=DAMAGE_BOOST_DEFAULT):
        if damage_boost <= 0:
            raise ValueError("The damage_boost parameter is less than or equal to 0!")

        super(DamageBoostPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)
        self.effects.append(DamageBoostPickupEffect)
        self.effects.append(self.delete)
        self.damage_boost = damage_boost

    def apply(self, avatar=None, cell=None, region=None):
        self.effects[0](self.damage_boost, avatar)
        self.effects[1]()

    def __repr__(self):
        return 'DamageBoostPickup(damage_boost={})'.format(self.damage_boost)

    def serialise(self):
        return {
                'type': 'damage_boost',
                'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
                }
        }


def serialise_pickups(world_map):
    return [cell.pickup.serialise() for cell in world_map.pickup_cells()]


ALL_PICKUPS = (
    HealthPickup,
    InvulnerabilityPickup,
    DamageBoostPickup,
)
