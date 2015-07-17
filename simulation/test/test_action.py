import unittest

from simulation.avatar import Avatar
from simulation.location import Location
from simulation import direction
from simulation.test.dummy_player import DummyPlayer
from simulation.test.maps import InfiniteMap, EmptyMap
from simulation.world_state import WorldState
from simulation.action import *
from simulation.avatar_manager import AvatarManager


ORIGIN = Location(row=0, col=0)
RIGHT_OF_ORIGIN = Location(row=0, col=1)
ABOVE_ORIGIN = Location(row=-1, col=0)


class TestAction(unittest.TestCase):
    def setUp(self):
        player = DummyPlayer()
        self.avatar = Avatar(ORIGIN, player)
        self.other_avatar = Avatar(RIGHT_OF_ORIGIN, player)
        self.avatar_manager = AvatarManager([self.avatar, self.other_avatar])

    def test_successful_move_action(self):
        world_state = WorldState(InfiniteMap(), self.avatar_manager)
        MoveAction(direction.NORTH).apply(world_state, self.avatar)

        self.assertEqual(self.avatar.location, ABOVE_ORIGIN)
        self.assertEqual(self.avatar.events,
                         [MovedEvent(ORIGIN, ABOVE_ORIGIN)])

    def test_failed_move_action(self):
        world_state = WorldState(EmptyMap(), self.avatar_manager)
        MoveAction(direction.NORTH).apply(world_state, self.avatar)

        self.assertEqual(self.avatar.location, ORIGIN)
        self.assertEqual(self.avatar.events,
                         [FailedMoveEvent(ORIGIN, ABOVE_ORIGIN)])

    def test_successful_attack_action(self):
        world_state = WorldState(InfiniteMap(), self.avatar_manager)
        AttackAction(direction.EAST).apply(world_state, self.avatar)

        target_location = RIGHT_OF_ORIGIN
        damage_dealt = 1

        self.assertEqual(self.avatar.location, ORIGIN)
        self.assertEqual(self.other_avatar.location, RIGHT_OF_ORIGIN)

        self.assertEqual(self.avatar.events,
                         [PerformedAttackEvent(
                             self.other_avatar,
                             target_location,
                             damage_dealt)])
        self.assertEqual(self.other_avatar.events,
                         [ReceivedAttackEvent(self.avatar, damage_dealt)])

    def test_failed_attack_action(self):
        world_state = WorldState(InfiniteMap(), self.avatar_manager)
        AttackAction(direction.NORTH).apply(world_state, self.avatar)

        target_location = ABOVE_ORIGIN

        self.assertEqual(self.avatar.location, ORIGIN)
        self.assertEqual(self.other_avatar.location, RIGHT_OF_ORIGIN)

        self.assertEqual(self.avatar.events,
                         [FailedAttackEvent(target_location)])
        self.assertEqual(self.other_avatar.events, [])
