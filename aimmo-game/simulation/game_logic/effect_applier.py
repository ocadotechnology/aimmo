from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.game_state import GameState

LOGGER = getLogger(__name__)


class EffectApplier:
    """
    Applier for all interactables on the WorldMap.

    Handles the checking if conditions are met, then applies any effects for interactables
    where this occurs.
    """

    def apply(self, game_state: "GameState"):
        """Apply interactable effects to any avatar that is on a pickup cell."""
        for cell in game_state.world_map.interactable_cells():
            if cell.interactable.conditions_met(game_state):
                cell.interactable.apply()
