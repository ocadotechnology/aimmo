from __future__ import absolute_import
import unittest

from simulation import event
from simulation.location import Location
from .dummy_avatar import DummyAvatarRunner
from .maps import InfiniteMap, EmptyMap, ScoreOnOddColumnsMap, AvatarMap
from simulation.game_state import GameState
from simulation import action
from simulation.avatar.avatar_manager import AvatarManager


ORIGIN = Location(x=0, y=0)
EAST_OF_ORIGIN = Location(x=1, y=0)
NORTH_OF_ORIGIN = Location(x=0, y=1)


class TestAction(unittest.TestCase):
    def setUp(self):
        self.avatar = DummyAvatarRunner(ORIGIN, player_id=1)
        self.other_avatar = DummyAvatarRunner(EAST_OF_ORIGIN, player_id=2)
        self.avatar_manager = AvatarManager()

    def test_successful_move_north_action(self):
        game_state = GameState(InfiniteMap(), self.avatar_manager)
        action.MoveAction({'x': 0, 'y': 1}).apply(game_state, self.avatar)

        self.assertEqual(self.avatar.location, NORTH_OF_ORIGIN)
        self.assertEqual(self.avatar.events, [event.MovedEvent(ORIGIN, NORTH_OF_ORIGIN)])

    def test_successful_move_east_action(self):
        game_state = GameState(InfiniteMap(), self.avatar_manager)
        action.MoveAction({'x': 1, 'y': 0}).apply(game_state, self.avatar)

        self.assertEqual(self.avatar.location, EAST_OF_ORIGIN)
        self.assertEqual(self.avatar.events, [event.MovedEvent(ORIGIN, EAST_OF_ORIGIN)])

    def test_failed_move_action(self):
        game_state = GameState(EmptyMap(), self.avatar_manager)
        action.MoveAction({'x': 0, 'y': 1}).apply(game_state, self.avatar)

        self.assertEqual(self.avatar.location, ORIGIN)
        self.assertEqual(self.avatar.events, [event.FailedMoveEvent(ORIGIN, NORTH_OF_ORIGIN)])

    def test_move_action_to_score_square(self):
        game_state = GameState(ScoreOnOddColumnsMap(), self.avatar_manager)
        self.assertEqual(self.avatar.score, 0)

        action.MoveAction({'x': 1, 'y': 0}).apply(game_state, self.avatar)
        self.assertEqual(self.avatar.score, 1)

        action.MoveAction({'x': 1, 'y': 0}).apply(game_state, self.avatar)
        self.assertEqual(self.avatar.score, 1)

        action.MoveAction({'x': 1, 'y': 0}).apply(game_state, self.avatar)
        self.assertEqual(self.avatar.score, 2)

    @unittest.skip("Implement after changes")
    def test_move_action_pickups(self):
        # TODO
        pass

    def test_successful_attack_action(self):
        game_state = GameState(AvatarMap(self.other_avatar), self.avatar_manager)
        action.AttackAction({'x': 0, 'y': 1}).apply(game_state, self.avatar)

        target_location = NORTH_OF_ORIGIN
        damage_dealt = 1

        self.assertEqual(self.avatar.location, ORIGIN)
        self.assertEqual(self.other_avatar.location, EAST_OF_ORIGIN)
        self.assertEqual(self.other_avatar.times_died, 0)
        self.assertEqual(self.other_avatar.health, 4)

        self.assertEqual(self.avatar.events,
                         [event.PerformedAttackEvent(
                             self.other_avatar,
                             target_location,
                             damage_dealt)])
        self.assertEqual(self.other_avatar.events,
                         [event.ReceivedAttackEvent(self.avatar, damage_dealt)])

    def test_failed_attack_action(self):
        game_state = GameState(InfiniteMap(), self.avatar_manager)
        action.AttackAction({'x': 0, 'y': 1}).apply(game_state, self.avatar)

        target_location = NORTH_OF_ORIGIN

        self.assertEqual(self.avatar.location, ORIGIN)
        self.assertEqual(self.other_avatar.location, EAST_OF_ORIGIN)
        self.assertEqual(self.avatar.events, [event.FailedAttackEvent(target_location)])
        self.assertEqual(self.other_avatar.events, [])

    def test_avatar_dies(self):
        self.other_avatar.health = 1
        game_state = GameState(AvatarMap(self.other_avatar), self.avatar_manager)
        action.AttackAction({'x': 0, 'y': 1}).apply(game_state, self.avatar)

        target_location = NORTH_OF_ORIGIN
        damage_dealt = 1
        self.assertEqual(self.avatar.events,
                         [event.PerformedAttackEvent(
                             self.other_avatar,
                             target_location,
                             damage_dealt)])
        self.assertEqual(self.other_avatar.events,
                         [event.ReceivedAttackEvent(self.avatar, damage_dealt)])

        self.assertEqual(self.avatar.location, ORIGIN)
        self.assertEqual(self.other_avatar.health, 0)
        self.assertEqual(self.other_avatar.times_died, 1)
        self.assertEqual(self.other_avatar.location, Location(10, 10))

    def test_no_move_in_wait(self):
        game_state = GameState(InfiniteMap(), self.avatar_manager)
        action.WaitAction().apply(game_state, self.avatar)
        self.assertEqual(self.avatar.location, ORIGIN)
