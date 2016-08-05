from __future__ import absolute_import
import unittest

from simulation.avatar.avatar_appearance import AvatarAppearance
from simulation.game_state import GameState
from simulation.location import Location
from simulation.turn_manager import TurnManager

from .maps import InfiniteMap
from .dummy_avatar import DummyAvatarRunner
from .dummy_avatar import DummyAvatarManager


ORIGIN = Location(x=0, y=0)

RIGHT_OF_ORIGIN = Location(x=1, y=0)
FIVE_RIGHT_OF_ORIGIN = Location(x=5, y=0)

ABOVE_ORIGIN = Location(x=0, y=1)
FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE = Location(x=5, y=1)


class TestTurnManager(unittest.TestCase):
    def construct_default_avatar_appearance(self):
        return AvatarAppearance("#000", "#ddd", "#777", "#fff")

    def construct_turn_manager(self, *avatars):
        self.avatar_manager = DummyAvatarManager(avatars)
        self.game_state = GameState(InfiniteMap(), self.avatar_manager)
        self.turn_manager = TurnManager(game_state=self.game_state,
                                        end_turn_callback=lambda: None,
                                        concurrent_turns=True)

    def test_run_turn(self):
        avatar = DummyAvatarRunner(ORIGIN, player_id=1)
        self.construct_turn_manager(avatar)
        self.turn_manager.run_turn()
        self.assertEqual(avatar.location, RIGHT_OF_ORIGIN)

    def test_run_several_turns(self):
        avatar = DummyAvatarRunner(ORIGIN, player_id=1)
        self.construct_turn_manager(avatar)
        [self.turn_manager.run_turn() for _ in range(5)]
        self.assertEqual(avatar.location, FIVE_RIGHT_OF_ORIGIN)

    def test_run_several_turns_and_avatars(self):
        avatar1 = DummyAvatarRunner(ORIGIN, player_id=1)
        avatar2 = DummyAvatarRunner(ABOVE_ORIGIN, player_id=2)
        self.construct_turn_manager(avatar1, avatar2)
        [self.turn_manager.run_turn() for _ in range(5)]
        self.assertEqual(avatar1.location, FIVE_RIGHT_OF_ORIGIN)
        self.assertEqual(avatar2.location, FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE)

    def test_move_chain(self):
        avatars = [DummyAvatarRunner(Location(x=x, y=0), player_id=x) for x in range(5)]
        self.construct_turn_manager(*avatars)
        self.turn_manager.run_turn()
        [self.assertEqual(avatars[x].location, Location(x=x + 1, y=0)) for x in range(5)]


if __name__ == '__main__':
    unittest.main()
