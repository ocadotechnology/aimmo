from logging import getLogger
LOGGER = getLogger(__name__)


class PickupApplier:
    def apply(self, worldmap: object):
        """ Applies pickup effects to any avatar that is on a pickup cell """
        for cell in worldmap.pickup_cells():
            if cell.pickup.conditions_met(worldmap):
                cell.pickup.apply(cell.avatar)
