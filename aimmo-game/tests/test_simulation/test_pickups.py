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

class TestDeliveryPickup(_BaseCases.BasePickupTestCase):
    pickup_class = pickups.DeliveryPickup

    def test_delivery_picked_up(self):
        self.assertEqual(self.avatar.pickups[pickups.DeliveryPickup], 0)
        self.apply_pickup()
        self.assertEqual(self.avatar.pickups[pickups.DeliveryPickup], 1)

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {'type': 'delivery'})
