from abc import ABCMeta, abstractmethod


class _Effect(object):
    __metaclass__ = ABCMeta

    def __init__(self, avatar):
        self._avatar = avatar

    @abstractmethod
    def turn(self):
        raise NotImplementedError()


class _TimedEffect(_Effect):
    __metaclass__ = ABCMeta
    EFFECT_TIME = 10

    def __init__(self, *args):
        super(_TimedEffect, self).__init__(*args)
        self._time_remaining = self.EFFECT_TIME

    def remove(self):
        self._avatar.effects.remove(self)

    def turn(self):
        self._time_remaining -= 1
        return self._time_remaining != 0


class InvulnerabilityEffect(_TimedEffect):
    def __init__(self, *args):
        super(InvulnerabilityEffect, self).__init__(*args)
        self._avatar.resistance += 1000

    def remove(self):
        super(InvulnerabilityEffect, self).remove()
        self._avatar.resistance -= 1000
