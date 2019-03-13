from abc import ABCMeta, abstractmethod, abstractproperty
from functools import reduce
from logging import getLogger
from typing import TYPE_CHECKING

import simulation.effects as effects
from simulation.pickups.conditions import TurnState, avatar_on_cell

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

    def __str__(self):
        return self.__class__.__name__

    def delete(self):
        self.cell.pickup = None

    def conditions_met(self, world_map: 'WorldMap'):
        turn_state = TurnState(world_map, self.cell)
        """ Applies logical AND on all conditions, returns True is all conditions are met. """
        return all([condition(turn_state) for condition in self.conditions])

    def apply(self, avatar):
        self._apply(avatar)
        self.delete()

    @abstractmethod
    def _apply(self, avatar):
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

    def _apply(self, avatar):
        avatar.health += self.health_restored

        # Make sure the health is capped at 100.
        if avatar.health > AVATAR_HEALTH_MAX:
            avatar.health = AVATAR_HEALTH_MAX


class _PickupEffect(_Pickup):
    __metaclass__ = ABCMeta

    def __init__(self, *args):
        super(_PickupEffect, self).__init__(*args)
        self.params = []

    @abstractproperty
    def EFFECT(self):
        raise NotImplementedError()

    def _apply(self, avatar):
        self.params.append(avatar)
        avatar.effects.add(self.EFFECT(*self.params))


class InvulnerabilityPickup(_PickupEffect):
    EFFECT = effects.InvulnerabilityPickupEffect

    def __init__(self, cell):
        super(InvulnerabilityPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)

    def serialise(self):
        return {
                'type': 'invulnerability',
                'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
                }
        }


class DamageBoostPickup(_PickupEffect):
    EFFECT = effects.DamageBoostPickupEffect

    def __init__(self, cell, damage_boost=DAMAGE_BOOST_DEFAULT):
        if damage_boost <= 0:
            raise ValueError("The damage_boost parameter is less than or equal to 0!")

        super(DamageBoostPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)
        self.damage_boost = damage_boost
        self.params.append(self.damage_boost)

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


def serialize_pickups(world_map):
    return [cell.pickup.serialise() for cell in world_map.pickup_cells()]


ALL_PICKUPS = (
    HealthPickup,
    InvulnerabilityPickup,
    DamageBoostPickup,
)
