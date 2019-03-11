"""

"""
import math
from abc import ABCMeta, abstractmethod

DEFAULT_EFFECT_TIME = 10

INVULNERABILITY_RESISTANCE = 1000
DAMAGE_BOOST_DEFAULT = 5

HEALTH_RESTORE_DEFAULT = 3
HEALTH_RESTORE_MAX = 100
AVATAR_HEALTH_MAX = 100


class _Effect(object):
    def __init__(self, recipient, duration=DEFAULT_EFFECT_TIME):
        self._recipient = recipient
        self.is_expired = False
        self._time_remaining = duration
        try:
            self._recipient.effects.add(self)
        except KeyError as e:
            raise KeyError("The target object does support effects.")

    def on_turn(self):
        self._time_remaining -= 1
        if self._time_remaining <= 0:
            self.is_expired = True

    def remove(self):
        try:
            self._recipient.effects.remove(self)
        except KeyError as e:
            raise KeyError(
                "The target object does not exist! Cannot remove the effect.")


class InvulnerabilityPickupEffect(_Effect):
    def __init__(self, *args):
        super(InvulnerabilityPickupEffect, self).__init__(*args)
        self._recipient.resistance += INVULNERABILITY_RESISTANCE

    def remove(self):
        super(InvulnerabilityPickupEffect, self).remove()
        self._recipient.resistance -= INVULNERABILITY_RESISTANCE

    def __repr__(self):
        return f'InvulnerabilityPickupEffect(value={INVULNERABILITY_RESISTANCE})'


class DamageBoostPickupEffect(_Effect):
    def __init__(self, *args):
        self._damage_boost = int(round(DAMAGE_BOOST_DEFAULT))
        super(DamageBoostPickupEffect, self).__init__(*args)
        self._recipient.attack_strength += self._damage_boost

    def remove(self):
        super(DamageBoostPickupEffect, self).remove()
        self._recipient.attack_strength -= self._damage_boost

    def __repr__(self):
        return f'DamageBoostPickupEffect(value={self._damage_boost})'


class HealthPickupEffect(_Effect):
    def __init__(self, *args):
        super(HealthPickupEffect, self).__init__(duration=1, *args)
        self.health_restored = HEALTH_RESTORE_DEFAULT
        self.give_health(self._recipient)

    def remove(self):
        super(HealthPickupEffect, self).remove()

    def give_health(self, avatar):
        avatar.health += self.health_restored

        # Make sure the health is capped at 100.
        if avatar.health > AVATAR_HEALTH_MAX:
            avatar.health = AVATAR_HEALTH_MAX

    def __repr__(self):
        return f'HealthPickupEffect(value={self.health_restored})'
