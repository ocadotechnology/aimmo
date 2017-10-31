from __future__ import absolute_import

import abc
from unittest import TestCase

from simulation import effects, pickups
from .dummy_avatar import DummyAvatar
from .maps import MockCell


class _BaseCases(object):
    class BasePickupTestCase(TestCase):
        __metaclass__ = abc.ABCMeta

        def setUp(self):
            self.avatar = DummyAvatar(1, None)
            self.cell = MockCell()
            self.pickup = self.pickup_class(self.cell)

        def set_custom_pickup(self, *args):
            self.pickup = self.pickup_class(self.cell, *args)

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

    def test_invulnerability_is_applied(self):
        self.apply_pickup()
        self.assertIsInstance(self.pickup, pickups.HealthPickup)

    def test_health_increases(self):
        self.apply_pickup()
        self.assertEqual(self.avatar.health, 8)

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {'type': 'health', 'health_restored': 3})

    def test_given_custom_health_pickup_increase_health_increases(self):
        # Test 1 - increase of 5
        self.assertEqual(self.avatar.health, 5)
        self.set_custom_pickup(5)

        self.apply_pickup()

        self.assertEqual(self.avatar.health, 10)

        # Test 2 - increase of 50
        self.avatar.health = 10
        self.set_custom_pickup(50)

        self.apply_pickup()

        self.assertEqual(self.avatar.health, 60)

    def test_health_argument_raises_exception_when_health_exceeded(self):
        self.assertRaises(ValueError, self.set_custom_pickup, 150)

    def test_health_argument_raises_exception_when_health_useless(self):
        self.assertRaises(ValueError, self.set_custom_pickup, 0)

    def test_health_argument_raises_exception_when_health_under(self):
        self.assertRaises(ValueError, self.set_custom_pickup, -50)

    def test_health_cannot_be_greater_than_100(self):
        self.assertEqual(self.avatar.health, 5)
        self.set_custom_pickup(100)

        self.apply_pickup()

        self.assertEqual(self.avatar.health, 100)

    def test_health_rounding_up_to_nearest_int(self):
        self.set_custom_pickup(9.5)
        self.assertEqual(self.pickup.health_restored, 10)


class TestInvulnerabilityPickup(_BaseCases.BasePickupEffectTestCase):
    pickup_class = pickups.InvulnerabilityPickup
    effect_class = effects.InvulnerabilityPickupEffect

    def test_invulnerability_is_applied(self):
        self.apply_pickup()
        self.assertIsInstance(self.pickup, pickups.InvulnerabilityPickup)

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {'type': 'invulnerability'})


class TestDamagePickup(_BaseCases.BasePickupEffectTestCase):
    pickup_class = pickups.DamagePickup
    effect_class = effects.DamagePickupEffect

    def test_damagepickup_is_applied(self):
        self.apply_pickup()
        self.assertIsInstance(self.pickup, pickups.DamagePickup)

    def test_damagepickup_default_params(self):
        self.assertEqual(len(self.avatar.effects), 0)
        self.apply_pickup()
        self.assertEqual(len(self.avatar.effects), 1)

    def test_serialise_default(self):
        self.assertEqual(self.pickup.serialise(), {'type': 'damage', 'damage_boost': 5})

    def test_serialise_custom(self):
        self.set_custom_pickup(20)
        self.assertEqual(self.pickup.serialise(), {'type': 'damage', 'damage_boost': 20})
