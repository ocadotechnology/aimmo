import unittest

from simulation.avatar import Avatar
from simulation.location import Location
from simulation import direction
from simulation.test.dummy_player import DummyPlayer
from simulation.test.maps import InfiniteMap, EmptyMap
from simulation.world_state import WorldState
from simulation.action import *
from simulation.avatar_manager import AvatarManager


class TestAction(unittest.TestCase):
    def setUp(self):
        player = DummyPlayer()
        self.avatar = Avatar(Location(0, 0), player)
        self.other_avatar = Avatar(Location(0, 1), player)
        self.avatar_manager = AvatarManager([self.avatar, self.other_avatar])

    def test_successful_move_action(self):
        world_state = WorldState(InfiniteMap(), self.avatar_manager)
        MoveAction(direction.NORTH).apply(world_state, self.avatar)

        self.assertEqual(self.avatar.location, Location(0, 1))
        self.assertEqual(self.avatar.events,
                         [MovedEvent(Location(0, 0), Location(0, 1))])

    def test_failed_move_action(self):
        world_state = WorldState(EmptyMap(), self.avatar_manager)
        MoveAction(direction.NORTH).apply(world_state, self.avatar)

        self.assertEqual(self.avatar.location, Location(0, 0))
        self.assertEqual(self.avatar.events,
                         [FailedMoveEvent(Location(0, 0), Location(0, 1))])

    def test_successful_attack_action(self):
        world_state = WorldState(InfiniteMap(), self.avatar_manager)
        AttackAction(direction.NORTH).apply(world_state, self.avatar)

        target_location = Location(0, 1)
        damage_dealt = 1

        self.assertEqual(self.avatar.location, Location(0, 0))
        self.assertEqual(self.other_avatar.location, Location(0, 1))

        self.assertEqual(self.avatar.events,
                         [PerformedAttackEvent(self.other_avatar, target_location, damage_dealt)])
        self.assertEqual(self.other_avatar.events,
                         [ReceivedAttackEvent(self.avatar, damage_dealt)])

    def test_failed_attack_action(self):
        world_state = WorldState(InfiniteMap(), self.avatar_manager)
        AttackAction(direction.EAST).apply(world_state, self.avatar)

        target_location = Location(1, 0)

        self.assertEqual(self.avatar.location, Location(0, 0))
        self.assertEqual(self.other_avatar.location, Location(0, 1))

        self.assertEqual(self.avatar.events,
                         [FailedAttackEvent(target_location)])
        self.assertEqual(self.other_avatar.events, [])
