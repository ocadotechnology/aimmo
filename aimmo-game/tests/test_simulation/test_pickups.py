from __future__ import absolute_import

import abc
from unittest import TestCase

from simulation import pickups
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


class TestDeliveryPickup(_BaseCases.BasePickupTestCase):
    pickup_class = pickups.DeliveryPickup

    def test_delivery_picked_up(self):
        self.assertEqual(self.avatar.pickups[pickups.DeliveryPickup], 0)
        self.apply_pickup()
        self.assertEqual(self.avatar.pickups[pickups.DeliveryPickup], 1)

    def test_serialise(self):
        self.assertEqual(self.pickup.serialise(), {'type': 'delivery'})
