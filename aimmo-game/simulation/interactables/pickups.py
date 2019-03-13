from functools import reduce
from logging import getLogger
from typing import TYPE_CHECKING, List

from simulation.interactables.conditions import TurnState, avatar_on_cell
from simulation.interactables.effects import (DamageBoostEffect, HealthEffect,
                                              InvulnerabilityEffect)
from simulation.interactables.interactable import _Interactable

if TYPE_CHECKING:
    from simulation.game_state import GameState
    from simulation.avatar.avatar_wrapper import AvatarWrapper

LOGGER = getLogger(__name__)


class HealthPickup(_Interactable):
    def __init__(self, cell):
        super(HealthPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)

        self.effects.append(HealthEffect)

    def get_targets(self):
        return [
            self.cell.avatar
        ]

    def __repr__(self):
        return 'HealthPickup(Location={})'.format(self.cell.location)

    def serialize(self):
        return {
            'type': 'health',
            'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
            }
        }


class InvulnerabilityPickup(_Interactable):
    def __init__(self, cell):
        super(InvulnerabilityPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)

        self.effects.append(InvulnerabilityEffect)

    def get_targets(self):
        return [
            self.cell.avatar
        ]

    def __repr__(self):
        return 'InvulnerabilityPickup(Location={})'.format(self.cell.location)

    def serialize(self):
        return {
            'type': 'invulnerability',
            'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
            }
        }


class DamageBoostPickup(_Interactable):
    def __init__(self, cell):
        super(DamageBoostPickup, self).__init__(cell)
        self.conditions.append(avatar_on_cell)

        self.effects.append(DamageBoostEffect)

    def get_targets(self):
        return [
            self.cell.avatar
        ]

    def __repr__(self):
        return 'DamageBoostPickup(Location={})'.format(self.cell.location)

    def serialize(self):
        return {
            'type': 'damage_boost',
            'location': {
                    'x': self.cell.location.x,
                    'y': self.cell.location.y,
            }
        }


def serialize_pickups(world_map):
    return [cell.interactable.serialize() for cell in world_map.pickup_cells()]


ALL_PICKUPS = (
    HealthPickup,
    InvulnerabilityPickup,
    DamageBoostPickup,
)
