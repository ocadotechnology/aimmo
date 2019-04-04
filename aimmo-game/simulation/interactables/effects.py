"""
This module contains all currently availible effects.

Effects are applied to all targets specified by a pickup
When creating effects they should follow the same basic format:

```python

class NewEffect(_Effect):
    def __init__(self, *args):
        super(NewEffect, self).__init__(duration=X,*args)
        # what the effect does goes here

    def remove(self):
        super(NewEffect, self).remove()
        # if the effect is temporary, it should be undone here
```
"""
import math
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.avatar.avatar_wrapper import AvatarWrapper

DEFAULT_EFFECT_TIME = 10

INVULNERABILITY_RESISTANCE = 1000
DAMAGE_BOOST_DEFAULT = 5

HEALTH_RESTORE_DEFAULT = 3
HEALTH_RESTORE_MAX = 100
AVATAR_HEALTH_MAX = 100

SCORE_INCREASE_DEFAULT = 1


class _Effect(object):
    """
    Base effect class, does nothing on its own.
    """

    def __init__(self, recipient: "AvatarWrapper", duration=DEFAULT_EFFECT_TIME):
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
                "The target object does not exist! Cannot remove the effect."
            )


class InvulnerabilityEffect(_Effect):
    def __init__(self, *args):
        super(InvulnerabilityEffect, self).__init__(*args)
        self._recipient.resistance += INVULNERABILITY_RESISTANCE

    def remove(self):
        super(InvulnerabilityEffect, self).remove()
        self._recipient.resistance -= INVULNERABILITY_RESISTANCE

    def __repr__(self):
        return f"InvulnerabilityEffect(value={INVULNERABILITY_RESISTANCE})"


class DamageBoostEffect(_Effect):
    def __init__(self, *args):
        self._damage_boost = int(round(DAMAGE_BOOST_DEFAULT))
        super(DamageBoostEffect, self).__init__(*args)
        self._recipient.attack_strength += self._damage_boost

    def remove(self):
        super(DamageBoostEffect, self).remove()
        self._recipient.attack_strength -= self._damage_boost

    def __repr__(self):
        return f"DamageBoostEffect(value={self._damage_boost})"


class HealthEffect(_Effect):
    def __init__(self, *args):
        super(HealthEffect, self).__init__(duration=1, *args)
        self.health_restored = HEALTH_RESTORE_DEFAULT
        self.give_health(self._recipient)

    def remove(self):
        super(HealthEffect, self).remove()

    def give_health(self, avatar):
        avatar.health += self.health_restored

        # Make sure the health is capped at 100.
        if avatar.health > AVATAR_HEALTH_MAX:
            avatar.health = AVATAR_HEALTH_MAX

    def __repr__(self):
        return f"HealthEffect(value={self.health_restored})"


class ScoreEffect(_Effect):
    def __init__(self, *args):
        super(ScoreEffect, self).__init__(duration=1, *args)
        self.score_given = SCORE_INCREASE_DEFAULT
        self._recipient.score += self.score_given

    def remove(self):
        super(ScoreEffect, self).remove()

    def __repr__(self):
        return f"ScoreEffect(value={self.score_given})"
