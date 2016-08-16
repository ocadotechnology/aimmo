from __future__ import absolute_import
import abc
from .dummy_avatar import DummyAvatarRunner
from simulation import effects
from unittest import TestCase


class _BaseCases(object):
    class BaseTimedEffectTestCase(TestCase):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def make_effect(self, avatar):
            pass

        def setUp(self):
            self.avatar = DummyAvatarRunner(None, 1)
            self.effect = self.make_effect(self.avatar)
            self.avatar.effects.add(self.effect)

        def assertNoEffects(self):
            self.assertEqual(len(list(self.avatar.effects)), 0)

        def test_effect_removed(self):
            self.effect.remove()
            self.assertNoEffects()

        def test_effect_expires(self):
            for _ in xrange(10):
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


class TestDamageEffect(_BaseCases.BaseTimedEffectTestCase):
    def make_effect(self, *args):
        return effects.DamagePickupEffect(5, *args)

    def test_damage_increases(self):
        self.assertEqual(self.avatar.attack_strength, 6)

    def test_damage_decreases(self):
        self.effect.remove()
        self.assertEqual(self.avatar.attack_strength, 1)
