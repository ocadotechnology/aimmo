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
        # Round the value to the nearest integer.
        health_restored = int(round(health_restored))

        # Check if the value provided is legal.
        if 0 < health_restored <= 100:
            super(HealthPickup, self).__init__(cell)
            self.health_restored = health_restored
        else:
            raise ValueError("Health Restored has to be within 0-100 range!")

    def __repr__(self):
        return 'HealthPickup(health_restored={})'.format(self.health_restored)

    def serialise(self):
        return {
                'type': 'health',
                'health_restored': self.health_restored,
        }

    def _apply(self, avatar):
        avatar.health += self.health_restored

        # Make sure the health is capped at 100.
        if avatar.health > 100:
            avatar.health = 100


class _PickupEffect(_Pickup):
    __metaclass__ = ABCMeta

    def __init__(self, *args):
        super(_PickupEffect, self).__init__(*args)
        self.params = []

    @abstractproperty
    def EFFECT(self):
        raise NotImplementedError()

    def _apply(self, avatar):
        self.params.append(avatar)
        avatar.effects.add(self.EFFECT(*self.params))


class InvulnerabilityPickup(_PickupEffect):
    EFFECT = effects.InvulnerabilityPickupEffect

    def serialise(self):
        return {
                'type': 'invulnerability',
        }


class DamagePickup(_PickupEffect):
    EFFECT = effects.DamagePickupEffect

    def __init__(self, cell, damage_boost=5):
        super(DamagePickup, self).__init__(cell)
        self.damage_boost = damage_boost
        self.params.append(self.damage_boost)

    def __repr__(self):
        return 'DamagePickup(damage_boost={})'.format(self.damage_boost)

    def serialise(self):
        return {
                'type': 'damage',
                'damage_boost': self.damage_boost,
        }


ALL_PICKUPS = (
    HealthPickup,
    InvulnerabilityPickup,
    DamagePickup,
)
