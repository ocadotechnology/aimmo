from abc import ABCMeta, abstractmethod, abstractproperty
from functools import reduce
from logging import getLogger
from typing import TYPE_CHECKING

from simulation.pickups.conditions import TurnState, avatar_on_cell
from simulation.pickups.effects import (DamageBoostPickupEffect,
                                        HealthPickupEffect,
                                        InvulnerabilityPickupEffect)

if TYPE_CHECKING: 
    from simulation.game_state import GameState

LOGGER = getLogger(__name__)


class _Pickup(object):
    __metaclass__ = ABCMeta

    def __init__(self, cell):
        self.cell = cell
        self.conditions = []
        self.effects = []

    def __str__(self):
        return self.__class__.__name__

    def delete(self, turn_state):
        self.cell.pickup = None

    def conditions_met(self, game_state: 'GameState'):
        """Apply logical and on all conditions, returns True is all conditions are met."""
        turn_state = TurnState(game_state, self.cell)
        return all([condition(turn_state) for condition in self.conditions])

    def apply(self, game_state: 'GameState'):
        """Apply all effects in sequential order."""
        turn_state = TurnState(game_state, self.cell)
        for effect in self.effects:
            effect(turn_state)

    @abstractmethod
    def serialise(self):
        raise NotImplementedError()


class HealthPickup(_Pickup):
    def __init__(self, cell):
        super(HealthPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)
        self.effects.append(HealthPickupEffect)
        self.effects.append(self.delete)

    def __repr__(self):
        return 'HealthPickup(Location={})'.format(self.cell.location)

    def serialise(self):
        return {
                'type': 'health',
                'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
                }
        }


class InvulnerabilityPickup(_Pickup):
    def __init__(self, cell):
        super(InvulnerabilityPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)
        self.effects.append(InvulnerabilityPickupEffect)
        self.effects.append(self.delete)

    def __repr__(self):
        return 'InvulnerabilityPickup(Location={})'.format(self.cell.location)

    def serialise(self):
        return {
                'type': 'invulnerability',
                'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
                }
        }


class DamageBoostPickup(_Pickup):
    def __init__(self, cell):
        super(DamageBoostPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)
        self.effects.append(DamageBoostPickupEffect)
        self.effects.append(self.delete)

    def __repr__(self):
        return 'DamageBoostPickup(Location={})'.format(self.cell.location)

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
