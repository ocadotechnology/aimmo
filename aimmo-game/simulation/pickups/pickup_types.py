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
        self.targets = []

    def __str__(self):
        return self.__class__.__name__

    def delete(self):
        self.cell.pickup = None

    def conditions_met(self, game_state: 'GameState'):
        """Apply logical and on all conditions, returns True is all conditions are met."""
        turn_state = TurnState(game_state, self.cell)
        return all([condition(turn_state) for condition in self.conditions])

    
    def apply(self):
        """
        Apply all effects in sequential order.
        
        Targets for effects can be a single object, or a list of objects. all
        targets must have an 'effect' attribute that is of type=set.
        """
        self.targets = self.get_targets()
        for effect, target in zip(self.effects, self.targets):
            if isinstance(type(target), list):
                for sub_target in target:
                    effect(sub_target)
            else:
                effect(target)

    @abstractmethod
    def serialise(self):
        raise NotImplementedError()

    @abstractmethod
    def get_targets(self):
        raise NotImplementedError()


class HealthPickup(_Pickup):
    def __init__(self, cell):
        super(HealthPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)

        self.effects.append(HealthPickupEffect)
        self.effects.append(self.delete)
        
    def get_targets(self):
        return [
            self.cell.avatar,
        ]


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

    def get_targets(self):
        return [
            self.cell.avatar,
        ]

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

    def get_targets(self):
        return [
            self.cell.avatar,
        ]

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
