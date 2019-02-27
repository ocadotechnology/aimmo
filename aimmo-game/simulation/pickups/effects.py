from abc import ABCMeta, abstractmethod

import math

INVULNERABILITY_RESISTANCE = 1000


class _Effect(object):
    __metaclass__ = ABCMeta

    def __init__(self, target):
        self._target = target
        self.is_expired = False
        self._target.effects.add(self)

    @abstractmethod
    def on_turn(self):
        raise NotImplementedError()


class _TimedEffect(_Effect):
    __metaclass__ = ABCMeta
    EFFECT_TIME = 10

    def __init__(self, *args):
        super(_TimedEffect, self).__init__(*args)
        self._time_remaining = self.EFFECT_TIME

    def remove(self):
        try:
            self._target.effects.remove(self)
        except KeyError as e:
            raise KeyError("The target object does not exist! Cannot remove the effect.")

    def on_turn(self):
        self._time_remaining -= 1
        if self._time_remaining <= 0:
            self.is_expired = True


class InvulnerabilityPickupEffect(_TimedEffect):
    def __init__(self, *args):
        super(InvulnerabilityPickupEffect, self).__init__(*args)
        self._target.resistance += INVULNERABILITY_RESISTANCE

    def remove(self):
        super(InvulnerabilityPickupEffect, self).remove()
        self._target.resistance -= INVULNERABILITY_RESISTANCE


class DamageBoostPickupEffect(_TimedEffect):
    def __init__(self, damage_boost, *args):
        assert not math.isinf(damage_boost)

        self._damage_boost = int(round(damage_boost))
        super(DamageBoostPickupEffect, self).__init__(*args)
        self._target.attack_strength += self._damage_boost

    def remove(self):
        super(DamageBoostPickupEffect, self).remove()
        self._target.attack_strength -= self._damage_boost
