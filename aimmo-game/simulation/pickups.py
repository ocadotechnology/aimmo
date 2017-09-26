from abc import ABCMeta, abstractmethod, abstractproperty


class _Pickup(object):
    __metaclass__ = ABCMeta

    def __init__(self, cell):
        self.cell = cell

    def __str__(self):
        return self.__class__.__name__

    def delete(self):
        '''
        Deletes the pickup from the /CELL/.
        '''
        self.cell.pickup = None

    def apply(self, avatar):
        '''
        Public method to apply the pickup to an avatar. This will vary from type of pickup
        therefore implementation is done privately.
        :param avatar: an Avatar object.
        '''
        self._apply(avatar)
        self.delete()

    @abstractmethod
    def _apply(self, avatar):
        raise NotImplementedError()

    @abstractmethod
    def serialise(self):
        raise NotImplementedError()


class DeliveryPickup(_Pickup):
    '''
    Inherits generic functionality from _Pickup and needs to implement abstract methods.
    '''

    def __init__(self, cell):
        super(DeliveryPickup, self).__init__(cell)

    def _apply(self, avatar):
        avatar.pickups[DeliveryPickup] += 1 # Add a single count of this item.

    def __repr__(self):
        return 'DeliveryPickup'

    def serialise(self):
        return {
                'type': 'delivery'
        }


ALL_PICKUPS = (
    DeliveryPickup,
)
