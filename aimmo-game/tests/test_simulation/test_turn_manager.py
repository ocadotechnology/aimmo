from __future__ import absolute_import

import unittest

from simulation.avatar.avatar_appearance import AvatarAppearance
from simulation.game_state import GameState
from simulation.location import Location
from simulation.turn_manager import ConcurrentTurnManager
from simulation.logs import Logs

from .dummy_avatar import (DummyAvatarManager, MoveEastDummy, MoveNorthDummy,
                           MoveSouthDummy, MoveWestDummy, WaitDummy, DeadDummy)
from .maps import InfiniteMap
from .mock_communicator import MockCommunicator

ORIGIN = Location(0, 0)

RIGHT_OF_ORIGIN = Location(1, 0)
FIVE_RIGHT_OF_ORIGIN = Location(5, 0)

ABOVE_ORIGIN = Location(0, 1)
FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE = Location(5, 1)


class MockGameState(GameState):
    def get_state_for(self, avatar):
        return self


class TestTurnManager(unittest.TestCase):
    """
        Key:
            > : Avatar moving eastward
            < : Avatar moving westward
            x : Avatar waiting / blocked
            o : Avatar successfully moved
            ! : Dead avatar (that should be waiting)
    """

    def construct_default_avatar_appearance(self):
        return AvatarAppearance("#000", "#ddd", "#777", "#fff")

    def construct_turn_manager(self, avatars, locations):
        self.avatar_manager = DummyAvatarManager(avatars)
        self.game_state = MockGameState(InfiniteMap(), self.avatar_manager)
        self.turn_manager = ConcurrentTurnManager(game_state=self.game_state,
                                                  end_turn_callback=lambda: None,
                                                  communicator=MockCommunicator(),
                                                  logs=Logs(),
                                                  have_avatars_code_updated={})
        for index, location in enumerate(locations):
            self.game_state.add_avatar(index, "", location)
        return self.turn_manager

    def assert_at(self, avatar, location):
        self.assertEqual(avatar.location, location)
        cell = self.game_state.world_map.get_cell(location)
        self.assertEqual(cell.avatar, avatar)

    def get_avatar(self, player_id):
        return self.avatar_manager.get_avatar(player_id)

    def run_turn(self):
        self.turn_manager.run_turn()

    def test_run_turn(self):
        """
        Given:  > _
        (1)
        Expect: _ o
        """
        self.construct_turn_manager([MoveEastDummy], [ORIGIN])
        avatar = self.get_avatar(0)

        self.assert_at(avatar, ORIGIN)
        self.run_turn()
        self.assert_at(avatar, RIGHT_OF_ORIGIN)

    def test_run_several_turns(self):
        """
        Given:  > _ _ _ _ _
        (5)
        Expect: _ _ _ _ _ o
        """
        self.construct_turn_manager([MoveEastDummy], [ORIGIN])
        avatar = self.get_avatar(0)

        self.assertEqual(avatar.location, ORIGIN)
        [self.run_turn() for _ in range(5)]
        self.assertEqual(avatar.location, FIVE_RIGHT_OF_ORIGIN)

    def test_run_several_turns_and_avatars(self):
        """
        Given:  > _ _ _ _ _
                > _ _ _ _ _
        (5)
        Expect: _ _ _ _ _ o
                _ _ _ _ _ o
        """
        self.construct_turn_manager([MoveEastDummy, MoveEastDummy],
                                    [ORIGIN,        ABOVE_ORIGIN])
        avatar0 = self.get_avatar(0)
        avatar1 = self.get_avatar(1)

        self.assert_at(avatar0, ORIGIN)
        self.assert_at(avatar1, ABOVE_ORIGIN)
        [self.run_turn() for _ in range(5)]
        self.assert_at(avatar0, FIVE_RIGHT_OF_ORIGIN)
        self.assert_at(avatar1, FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE)

    def test_move_chain_succeeds(self):
        """
        Given:  > > > > > _

        Expect: _ o o o o o
        """
        self.construct_turn_manager([MoveEastDummy for _ in range(5)],
                                    [Location(x, 0) for x in range(5)])
        avatars = [self.get_avatar(i) for i in range(5)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(5)]
        self.run_turn()
        [self.assert_at(avatars[x], Location(x + 1, 0)) for x in range(5)]

    def test_move_chain_fails_occupied(self):
        """
        Given:  > > x _

        Expect: x x x _
        """
        self.construct_turn_manager([MoveEastDummy, MoveEastDummy, WaitDummy],
                                    [Location(x, 0) for x in range(3)])
        avatars = [self.get_avatar(i) for i in range(3)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]
        self.run_turn()
        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]

    def test_move_chain_fails_occupied_by_dead_avatar(self):
        """
        Given: > > ! _

        Expect: x x ! _
        """

        self.construct_turn_manager([MoveEastDummy, MoveEastDummy, DeadDummy], [Location(x, 0) for x in range(3)])
        avatars = [self.get_avatar(i) for i in range(3)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]
        self.run_turn()
        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]

    def test_move_fails_collision(self):
        """
        Given: > _ <
        Expect: x _ x
        """

        self.construct_turn_manager([MoveEastDummy, MoveWestDummy], [Location(0, 0), Location(2, 0)])
        avatars = [self.get_avatar(i) for i in range(2)]

        self.assert_at(avatars[0], Location(0, 0))
        self.assert_at(avatars[1], Location(2, 0))

        self.run_turn()

        self.assert_at(avatars[0], Location(0, 0))
        self.assert_at(avatars[1], Location(2, 0))

    def test_move_chain_fails_collision(self):
        """
        Given:  > > > _ <
        (1)
        Expect: x x x _ x
        """
        locations = [Location(0, 0), Location(1, 0), Location(2, 0), Location(4, 0)]
        self.construct_turn_manager(
            [MoveEastDummy, MoveEastDummy, MoveEastDummy, MoveWestDummy],
            locations)
        avatars = [self.get_avatar(i) for i in range(4)]

        [self.assert_at(avatars[i], locations[i]) for i in range(4)]
        self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(4)]

    def test_move_chain_fails_cycle(self):
        """
        Given:  > v
                ^ <
        (1)
        Expect: x x
                x x
        """
        locations = [Location(0, 1), Location(1, 1), Location(1, 0), Location(0, 0)]
        self.construct_turn_manager(
            [MoveEastDummy, MoveSouthDummy, MoveWestDummy, MoveNorthDummy],
            locations)
        avatars = [self.get_avatar(i) for i in range(4)]

        [self.assert_at(avatars[i], locations[i]) for i in range(4)]
        self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(4)]

    def test_move_chain_fails_spiral(self):
        """
        Given:  > > v
                  ^ <
        (1)
        Expect: x x x
                  x x
        """
        locations = [Location(0, 1),
                     Location(1, 1),
                     Location(2, 1),
                     Location(2, 0),
                     Location(1, 0)]
        self.construct_turn_manager(
            [MoveEastDummy, MoveEastDummy, MoveSouthDummy, MoveWestDummy, MoveNorthDummy],
            locations)
        avatars = [self.get_avatar(i) for i in range(5)]

        [self.assert_at(avatars[i], locations[i]) for i in range(5)]
        self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(5)]


if __name__ == '__main__':
    unittest.main()
