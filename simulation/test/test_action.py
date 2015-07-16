import unittest

from simulation.test.dummy_player import DummyPlayer
from simulation.location import Location
from simulation import direction
from simulation.test.maps import InfiniteMap, EmptyMap
from simulation.world_state import WorldState
from simulation.action import *
from simulation.player_manager import PlayerManager


class TestAction(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.player = DummyPlayer(Location(0, 0))
        self.other_player = DummyPlayer(Location(0, 1))
        self.player_manager = PlayerManager([self.player, self.other_player])

    def test_successful_move_action(self):
        world_state = WorldState(InfiniteMap(), self.player_manager)
        MoveAction(direction.NORTH).apply(world_state, self.player)

        self.assertEqual(self.player.location, Location(0, 1))
        self.assertEqual(self.player.events,
                         [MovedEvent(Location(0, 0), Location(0, 1))])

    def test_failed_move_action(self):
        world_state = WorldState(EmptyMap(), self.player_manager)
        MoveAction(direction.NORTH).apply(world_state, self.player)

        self.assertEqual(self.player.location, Location(0, 0))
        self.assertEqual(self.player.events,
                         [FailedMoveEvent(Location(0, 0), Location(0, 1))])

    def test_successful_attack_action(self):
        world_state = WorldState(InfiniteMap(), self.player_manager)
        AttackAction(direction.NORTH).apply(world_state, self.player)

        target_location = Location(0, 1)
        damage_dealt = 1

        self.assertEqual(self.player.location, Location(0, 0))
        self.assertEqual(self.other_player.location, Location(0, 1))

        self.assertEqual(self.player.events,
                         [PerformedAttackEvent(self.other_player, target_location, damage_dealt)])
        self.assertEqual(self.other_player.events,
                         [ReceivedAttackEvent(self.player, damage_dealt)])

    def test_failed_attack_action(self):
        world_state = WorldState(InfiniteMap(), self.player_manager)
        AttackAction(direction.EAST).apply(world_state, self.player)

        target_location = Location(1, 0)

        self.assertEqual(self.player.location, Location(0, 0))
        self.assertEqual(self.other_player.location, Location(0, 1))

        self.assertEqual(self.player.events,
                         [FailedAttackEvent(target_location)])
        self.assertEqual(self.other_player.events, [])
