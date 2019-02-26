from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.world_map import WorldMap
LOGGER = getLogger(__name__)


class PickupApplier:
    def apply(self, worldmap: 'WorldMap'):
        """ Applies pickup effects to any avatar that is on a pickup cell """
        for cell in worldmap.pickup_cells():
            if cell.pickup.conditions_met(worldmap):
                cell.pickup.apply(cell.avatar)
