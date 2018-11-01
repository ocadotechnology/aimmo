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

        def apply_second_pickup(self, pickup_two):
            pickup_two.apply(self.avatar)

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

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {
            'type': 'health',
            'location': {
                'x': 0,
                'y': 0,
            }
        })


class TestInvulnerabilityPickup(_BaseCases.BasePickupEffectTestCase):
    pickup_class = pickups.InvulnerabilityPickup
    effect_class = effects.InvulnerabilityPickupEffect

    def test_invulnerability_is_applied(self):
        self.apply_pickup()
        self.assertIsInstance(self.pickup, pickups.InvulnerabilityPickup)

    def test_second_invulnerability_can_be_picked_up(self):
        self.assertEqual(self.avatar.resistance, 0)
        second_pickup = self.pickup_class(MockCell())

        self.apply_pickup()
        self.assertEqual(self.avatar.resistance, 1000)
        self.apply_second_pickup(second_pickup)

        self.assertEqual(self.avatar.resistance, 2000)

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {
            'type': 'invulnerability',
            'location': {
                'x': 0,
                'y': 0,
            }
        })


class TestDamageBoostPickup(_BaseCases.BasePickupEffectTestCase):
    pickup_class = pickups.DamageBoostPickup
    effect_class = effects.DamageBoostPickupEffect

    def test_damage_boost_pickup_is_applied(self):
        self.apply_pickup()
        self.assertIsInstance(self.pickup, pickups.DamageBoostPickup)

    def test_damage_boost_pickup_default_params(self):
        self.assertEqual(len(self.avatar.effects), 0)
        self.apply_pickup()
        self.assertEqual(len(self.avatar.effects), 1)

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {
            'type': 'damage_boost',
            'location': {
                'x': 0,
                'y': 0,
            }
        })
