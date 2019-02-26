from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.world_map import WorldMap

LOGGER = getLogger(__name__)


class PickupApplier:
    """
    Applier for all pickups on the WorldMap.

    Handles the checking if conditions are met, then applies any effects for pickups
    where this occurs.
    """

    def apply(self, worldmap: 'WorldMap'):
        """ Applies pickup effects to any avatar that is on a pickup cell """
        for cell in worldmap.pickup_cells():
            if cell.pickup.conditions_met(worldmap):
                cell.pickup.apply(cell.avatar)
