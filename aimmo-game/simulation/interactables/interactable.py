from abc import ABCMeta, abstractmethod, abstractproperty
from typing import TYPE_CHECKING, List

from simulation.interactables.conditions import TurnState

if TYPE_CHECKING:
    from simulation.game_state import GameState
    from simulation.avatar.avatar_wrapper import AvatarWrapper


class _Interactable(object):
    __metaclass__ = ABCMeta

    def __init__(self, cell):
        self.cell = cell
        self.delete_after_effects_applied = False

        self.conditions = []
        self.effects = []
        self.targets = []

    def __str__(self):
        return self.__class__.__name__

    def delete(self):
        self.cell.interactable = None

    def conditions_met(self, game_state: "GameState") -> "bool":
        """Apply logical `AND` on all conditions, returns True if all conditions are met."""
        turn_state = TurnState(game_state, self.cell)
        return all([condition(turn_state) for condition in self.conditions])

    def apply(self):
        """
        Apply all effects in sequential order.

        Targets for effects can be a single object, or a list of objects. All
        targets must have an 'effect' attribute that is of type=set.
        """
        self.targets = self.get_targets()
        for effect in self.effects:
            for target in self.targets:
                effect(target)

        if self.delete_after_effects_applied:
            self.delete()

    @abstractmethod
    def serialize(self):
        raise NotImplementedError()

    @abstractmethod
    def get_targets(self) -> "List[AvatarWrapper]":
        raise NotImplementedError()
