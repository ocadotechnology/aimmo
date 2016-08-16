from __future__ import absolute_import
import abc
from .dummy_avatar import DummyAvatarRunner
from .maps import MockCell
from simulation import effects, pickups
from unittest import TestCase


class _BaseCases(object):
    class BasePickupTestCase(TestCase):
        __metaclass__ = abc.ABCMeta

        def setUp(self):
            self.avatar = DummyAvatarRunner(None, 1)
            self.cell = MockCell()
            self.pickup = self.pickup_class(self.cell)

        def apply_pickup(self):
            self.pickup.apply(self.avatar)

        def test_pickup_removed(self):
            self.apply_pickup()
            self.assertIs(self.cell.pickup, None)

        @abc.abstractproperty
        def pickup_class(self):
            pass

    class BasePickupEffectTestCase(BasePickupTestCase):
        __metaclass__ = abc.ABCMeta

        @abc.abstractproperty
        def effect_class(self):
            pass

        def test_effect_added(self):
            self.apply_pickup()
            self.assertEqual(len(self.avatar.effects), 1)
            self.assertIsInstance(list(self.avatar.effects)[0], self.effect_class)


class TestHealthPickup(_BaseCases.BasePickupTestCase):
    pickup_class = pickups.HealthPickup

    def test_health_increases(self):
        self.apply_pickup()
        self.assertEqual(self.avatar.health, 8)

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {'type': 'health', 'health_restored': 3})


class TestInvulnerabilityPickup(_BaseCases.BasePickupEffectTestCase):
    pickup_class = pickups.InvulnerabilityPickup
    effect_class = effects.InvulnerabilityPickupEffect

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {'type': 'invulnerability'})


class TestDamagePickup(_BaseCases.BasePickupEffectTestCase):
    pickup_class = pickups.DamagePickup
    effect_class = effects.DamagePickupEffect

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {'type': 'damage', 'damage_boost': 5})
