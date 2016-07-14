from abc import ABCMeta, abstractmethod, abstractproperty
import effects


class _Pickup(object):
    __metaclass__ = ABCMeta

    def __init__(self, cell):
        self.cell = cell

    def __str__(self):
        return self.__class__.__name__

    def delete(self):
        self.cell.pickup = None

    def apply(self, avatar):
        self._apply(avatar)
        self.delete()

    @abstractmethod
    def _apply(self, avatar):
        raise NotImplementedError()

    @abstractmethod
    def serialise(self):
        raise NotImplementedError()


class HealthPickup(_Pickup):
    def __init__(self, cell, health_restored=3):
        super(HealthPickup, self).__init__(cell)
        self.health_restored = health_restored

    def __repr__(self):
        return 'HealthPickup(health_restored={})'.format(self.health_restored)

    def serialise(self):
        return {
                'type': 'health',
                'health_restored': self.health_restored,
        }

    def _apply(self, avatar):
        avatar.health += self.health_restored


class _PickupEffect(_Pickup):
    __metaclass__ = ABCMeta

    @abstractproperty
    def EFFECT(self):
        raise NotImplementedError()

    def _apply(self, avatar):
        avatar.effects.add(self.EFFECT(avatar))


class InvulnerabilityPickup(_PickupEffect):
    EFFECT = effects.InvulnerabilityEffect

    def serialise(self):
        return {
                'type': 'invulnerability',
        }


ALL_PICKUPS = (
    HealthPickup,
    InvulnerabilityPickup,
)
