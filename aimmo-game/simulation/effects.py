from abc import ABCMeta, abstractmethod

class _Effect(object):
    """
        An Effect is a class that gets applicated once per turn.

        The effect is attached to the avatar. See pickups for more details.
    """
    __metaclass__ = ABCMeta

    def __init__(self, avatar):
        self._avatar = avatar
        self.is_expired = False

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
        self._avatar.effects.remove(self)

    def on_turn(self):
        self._time_remaining -= 1
        if self._time_remaining <= 0:
            self.is_expired = True


class InvulnerabilityPickupEffect(_TimedEffect):
    def __init__(self, *args):
        super(InvulnerabilityPickupEffect, self).__init__(*args)
        self._avatar.resistance += 1000

    def remove(self):
        super(InvulnerabilityPickupEffect, self).remove()
        self._avatar.resistance -= 1000


class DamagePickupEffect(_TimedEffect):
    def __init__(self, damage_boost, *args):
        self._damage_boost = damage_boost
        super(DamagePickupEffect, self).__init__(*args)
        self._avatar.attack_strength += self._damage_boost

    def remove(self):
        super(DamagePickupEffect, self).remove()
        self._avatar.attack_strength -= self._damage_boost
