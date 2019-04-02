from __future__ import absolute_import

import abc
from unittest import TestCase

from simulation.interactables import effects

from .dummy_avatar import DummyAvatar
from .maps import MockCell


class _BaseCases(object):
    class BaseEffectTestCase(TestCase):
        __metaclass__ = abc.ABCMeta

        @abc.abstractmethod
        def make_effect(self, avatar):
            pass

        def setUp(self):
            self.cell = MockCell()
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


class TestInvulnerabilityEffect(_BaseCases.BaseEffectTestCase):
    def make_effect(self, *args):
        return effects.InvulnerabilityEffect(*args)

    def test_resistance_increases(self):
        self.assertEqual(self.avatar.resistance, 1000)

    def test_resistance_decreases(self):
        self.effect.remove()
        self.assertEqual(self.avatar.resistance, 0)

    def test_resistance_cannot_be_removed_twice(self):
        self.effect.remove()
        self.assertRaises(KeyError, self.effect.remove)


class TestDamageBoostEffect(_BaseCases.BaseEffectTestCase):
    def make_effect(self, *args):
        return effects.DamageBoostEffect(*args)

    def test_damage_increases(self):
        self.assertEqual(self.avatar.attack_strength, 6)

    def test_damage_decreases(self):
        self.effect.remove()
        self.assertEqual(self.avatar.attack_strength, 1)

    def test_damage_cannot_be_removed_twice(self):
        self.effect.remove()
        self.assertRaises(KeyError, self.effect.remove)
