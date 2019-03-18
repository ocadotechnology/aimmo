from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.game_state import GameState

LOGGER = getLogger(__name__)


class PickupApplier:
    """
    Applier for all pickups on the WorldMap.

    Handles the checking if conditions are met, then applies any effects for pickups
    where this occurs.
    """

    def apply(self, game_state: 'GameState'):
        """ Applies pickup effects to any avatar that is on a pickup cell """
        for cell in game_state.world_map.pickup_cells():
            if cell.interactable.conditions_met(game_state):
                cell.interactable.apply()
