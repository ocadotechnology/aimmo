from logging import getLogger

LOGGER = getLogger(__name__)


class PickupApplier:
    def apply(self, worldmap: object):
        """ applys pickup affects to any avatar that is now on a pickup cell """
        for cell in worldmap.pickup_cells():
            if cell.avatar is not None:
                cell.pickup.apply(cell.avatar)
