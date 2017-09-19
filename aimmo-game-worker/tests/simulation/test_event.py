from __future__ import absolute_import
from unittest import TestCase

from simulation.event import ReceivedAttackEvent, PerformedAttackEvent
from simulation.event import FailedAttackEvent, MovedEvent
from simulation.event import FailedMoveEvent


class TestEvent(TestCase):

    def test_namedtuple_values_by_id(self):
        local_tuple = ReceivedAttackEvent(2, 5)
        self.assertEqual(local_tuple[0], 2)
        self.assertEqual(local_tuple[1], 5)

        local_tuple = PerformedAttackEvent(2, 5, 3)
        self.assertEqual(local_tuple[0], 2)
        self.assertEqual(local_tuple[1], 5)
        self.assertEqual(local_tuple[2], 3)

        local_tuple = FailedAttackEvent(2)
        self.assertEqual(local_tuple[0], 2)

        local_tuple = MovedEvent(1, 2)
        self.assertEqual(local_tuple[0], 1)
        self.assertEqual(local_tuple[1], 2)

        local_tuple = FailedMoveEvent(10, 20)
        self.assertEqual(local_tuple[0], 10)
        self.assertEqual(local_tuple[1], 20)

    def test_namedtuple_values_by_name(self):
        local_tuple = ReceivedAttackEvent(2, 5)
        self.assertEqual(local_tuple.attacking_avatar, 2)
        self.assertEqual(local_tuple.damage_dealt, 5)

        local_tuple = PerformedAttackEvent(2, 5, 3)
        self.assertEqual(local_tuple.attacked_avatar, 2)
        self.assertEqual(local_tuple.target_location, 5)
        self.assertEqual(local_tuple.damage_dealt, 3)

        local_tuple = FailedAttackEvent(2)
        self.assertEqual(local_tuple.target_location, 2)

        local_tuple = MovedEvent(1, 2)
        self.assertEqual(local_tuple.source_location, 1)
        self.assertEqual(local_tuple.target_location, 2)

        local_tuple = FailedMoveEvent(10, 20)
        self.assertEqual(local_tuple.source_location, 10)
        self.assertEqual(local_tuple.target_location, 20)
