from __future__ import absolute_import
import unittest

from simulation.action import MoveAction, AttackAction, WaitAction
from simulation.event import MovedEvent, FailedMoveEvent, PerformedAttackEvent, ReceivedAttackEvent, FailedAttackEvent, DeathEvent
from simulation.location import Location
from simulation.direction import NORTH, EAST, SOUTH, WEST
from simulation.game_state import GameState
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_settings import AVATAR_STARTING_HEALTH, DEFAULT_ATTACK_DAMAGE
from simulation.turn_manager import NO_OTHER_ACTIONS

from .dummy_avatar import DummyAvatarManager
from .dummy_avatar import DummyAvatar
from .maps import InfiniteMap, ScoreOnOddColumnsMap

ORIGIN = Location(x=0, y=0)


class TestAction(unittest.TestCase):
    def setUp(self, map_type=InfiniteMap):
        self.avatar_manager = DummyAvatarManager([DummyAvatar, DummyAvatar])
        self.game_state = GameState(map_type(), self.avatar_manager)

        self.game_state.add_avatar(1, '', ORIGIN)
        self.game_state.add_avatar(2, '', ORIGIN + EAST)

        self.av_1 = self.avatar_manager.get_avatar(1)
        self.av_2 = self.avatar_manager.get_avatar(2)

        self.assert_at(self.av_1, ORIGIN)
        self.assert_at(self.av_2, ORIGIN + EAST)

    def move(self, avatar, direction, other_actions=NO_OTHER_ACTIONS):
        MoveAction(avatar.user_id, avatar.location, direction.dict).process(self.game_state, other_actions)

    def attack(self, avatar, direction, other_actions=NO_OTHER_ACTIONS):
        AttackAction(avatar.user_id, avatar.location, direction.dict).process(self.game_state, other_actions)

    def assert_at(self, avatar, location):
        self.assertEqual(avatar.location, location)
        cell = self.game_state._world_map.get_cell(location)
        self.assertEqual(cell.avatar, avatar)

    def assert_event(self, avatar, event):
        try:
            last_event = avatar.events[-1]
        except IndexError:
            last_event = None
        self.assertEqual(last_event, event)

    def test_move_succeeds(self):
        self.assert_at(self.av_1, ORIGIN)

        self.move(self.av_1, NORTH)

        self.assert_at(self.av_1, ORIGIN + NORTH)
        self.assert_event(self.av_1, MovedEvent(ORIGIN, ORIGIN + NORTH))

    def test_move_fails_unhabitable(self):
        self.game_state._world_map.get_cell(ORIGIN + NORTH)._habitable = False

        self.assert_at(self.av_1, ORIGIN)

        self.move(self.av_1, NORTH)

        self.assert_at(self.av_1, ORIGIN)
        self.assert_event(self.av_1, FailedMoveEvent(ORIGIN, ORIGIN + NORTH))

    def test_move_fails_occupied(self):
        self.assert_at(self.av_1, ORIGIN)

        self.move(self.av_1, EAST)

        self.assert_at(self.av_1, ORIGIN)
        self.assert_event(self.av_1, FailedMoveEvent(ORIGIN, ORIGIN + EAST))

    def test_move_to_score_squares(self):
        self.setUp(map_type=ScoreOnOddColumnsMap)
        self.game_state.remove_avatar(2)

        self.assertEqual(self.av_1.score, 0)

        self.move(self.av_1, EAST)
        self.game_state._apply_score()

        self.assertEqual(self.av_1.score, 1)

        self.move(self.av_1, EAST)
        self.game_state._apply_score()

        self.assertEqual(self.av_1.score, 1)

        self.move(self.av_1, EAST)
        self.game_state._apply_score()

        self.assertEqual(self.av_1.score, 2)

    @unittest.skip("Implement after changes")
    def test_move_action_pickups(self):
        # TODO
        pass

    def test_attack_succeeds(self):
        self.assertEqual(self.av_2.health, AVATAR_STARTING_HEALTH)

        damage = DEFAULT_ATTACK_DAMAGE
        self.attack(self.av_1, EAST)

        self.assertEqual(self.av_2.health, AVATAR_STARTING_HEALTH - damage)

        self.assert_event(self.av_1, PerformedAttackEvent(self.av_2.user_id, ORIGIN + EAST, damage))
        self.assert_event(self.av_2, ReceivedAttackEvent(self.av_1.user_id, damage))

    def test_attack_fails_vacant(self):
        self.assertEqual(self.av_2.health, AVATAR_STARTING_HEALTH)

        self.attack(self.av_1, NORTH)

        self.assertEqual(self.av_2.health, AVATAR_STARTING_HEALTH)

        self.assert_event(self.av_1, FailedAttackEvent(ORIGIN + NORTH))

    def test_avatar_dies(self):
        self.av_2.health = DEFAULT_ATTACK_DAMAGE

        self.attack(self.av_1, EAST)

        self.assertEqual(self.av_2.health, 0)

        self.avatar_manager.process_deaths(self.game_state._world_map)

        self.assertEqual(self.av_2.health, AVATAR_STARTING_HEALTH)
        self.assert_event(self.av_2, DeathEvent(ORIGIN + EAST, self.av_2.location))

    def test_no_move_in_wait(self):
        WaitAction(self.av_1.user_id, self.av_1.location).process(self.game_state, NO_OTHER_ACTIONS)
        self.assertEqual(self.av_1.location, ORIGIN)
