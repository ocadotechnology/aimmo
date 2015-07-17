import unittest

from simulation.location import Location
from simulation.avatar_manager import AvatarManager
from simulation.turn_manager import TurnManager
from simulation.test.maps import InfiniteMap
from simulation.test.dummy_avatar import  DummyAvatarRunner
from simulation.world_state import WorldState

ORIGIN = Location(row=0, col=0)

RIGHT_OF_ORIGIN = Location(row=0, col=1)
FIVE_RIGHT_OF_ORIGIN = Location(row=0, col=5)

ABOVE_ORIGIN = Location(row=-1, col=0)
FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE = Location(row=-1, col=5)


class TestTurnManager(unittest.TestCase):
    def construct_turn_manager(self, *avatars):
        self.avatar_manager = AvatarManager(avatars)
        self.world_state = WorldState(InfiniteMap(), self.avatar_manager)
        self.turn_manager = TurnManager(self.world_state)

    def test_run_turn(self):
        avatar = DummyAvatarRunner(ORIGIN, player_id=1)
        self.construct_turn_manager(avatar)
        self.turn_manager.run_turn()
        self.assertEqual(avatar.location, RIGHT_OF_ORIGIN)

    def test_run_several_turns(self):
        avatar = DummyAvatarRunner(ORIGIN, player_id=1)
        self.construct_turn_manager(avatar)
        [self.turn_manager.run_turn() for _ in xrange(5)]
        self.assertEqual(avatar.location, FIVE_RIGHT_OF_ORIGIN)

    def test_run_several_turns_and_avatars(self):
        avatar1 = DummyAvatarRunner(ORIGIN, player_id=1)
        avatar2 = DummyAvatarRunner(ABOVE_ORIGIN, player_id=2)
        self.construct_turn_manager(avatar1, avatar2)
        [self.turn_manager.run_turn() for _ in xrange(5)]
        self.assertEqual(avatar1.location, FIVE_RIGHT_OF_ORIGIN)
        self.assertEqual(avatar2.location, FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE)

if __name__ == '__main__':
    unittest.main()
