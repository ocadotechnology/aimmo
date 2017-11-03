from __future__ import absolute_import

import abc
from unittest import TestCase

from simulation import effects
from .dummy_avatar import DummyAvatar


class _BaseCases(object):
    class BaseTimedEffectTestCase(TestCase):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def make_effect(self, avatar):
            pass

        def setUp(self):
            self.avatar = DummyAvatar(1, None)
            self.effect = self.make_effect(self.avatar)
            self.avatar.effects.add(self.effect)

        def assertNoEffects(self):
            self.assertEqual(len(list(self.avatar.effects)), 0)

        def test_effect_removed(self):
            self.effect.remove()
            self.assertNoEffects()

        def test_effect_expires(self):
            for _ in range(10):
                self.effect.on_turn()
            self.assertTrue(self.effect.is_expired)


class TestInvulnerabilityEffect(_BaseCases.BaseTimedEffectTestCase):
    def make_effect(self, *args):
        return effects.InvulnerabilityPickupEffect(*args)

    def test_resistance_increases(self):
        self.assertEqual(self.avatar.resistance, 1000)

    def test_resistance_decreases(self):
        self.effect.remove()
        self.assertEqual(self.avatar.resistance, 0)

    def test_resistance_cannot_be_removed_twice(self):
        self.effect.remove()
        self.assertRaises(KeyError, self.effect.remove)


class TestDamageBoostPickupEffect(_BaseCases.BaseTimedEffectTestCase):
    def make_effect(self, *args):
        return effects.DamageBoostPickupEffect(5, *args)

    def test_damage_increases(self):
        self.assertEqual(self.avatar.attack_strength, 6)

    def test_damage_decreases(self):
        self.effect.remove()
        self.assertEqual(self.avatar.attack_strength, 1)

    def test_damage_cannot_be_removed_twice(self):
        self.effect.remove()
        self.assertRaises(KeyError, self.effect.remove)
