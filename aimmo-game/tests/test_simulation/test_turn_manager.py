from __future__ import absolute_import

import unittest

from simulation.avatar.avatar_appearance import AvatarAppearance
from simulation.game_state import GameState
from simulation.geography.location import Location
from simulation.managers.turn_manager import ConcurrentTurnManager, SequentialTurnManager
from .dummy_avatar import DummyAvatarManager, MoveEastDummy, MoveNorthDummy
from .dummy_avatar import MoveSouthDummy, MoveWestDummy, WaitDummy
from .maps import InfiniteMap

ORIGIN = Location(0, 0)

RIGHT_OF_ORIGIN = Location(1, 0)
FIVE_RIGHT_OF_ORIGIN = Location(5, 0)

ABOVE_ORIGIN = Location(0, 1)
FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE = Location(5, 1)


class MockGameState(GameState):
    def get_state_for(self, avatar):
        return self


class TestTurnManager(unittest.TestCase):
    def construct_default_avatar_appearance(self):
        return AvatarAppearance("#000", "#ddd", "#777", "#fff")

    def construct_turn_manager(self, avatars, locations, manager):
        self.avatar_manager = DummyAvatarManager(avatars)
        self.game_state = MockGameState(InfiniteMap(), self.avatar_manager)
        self.turn_manager = manager(game_state=self.game_state,
                                                  end_turn_callback=lambda: None,
                                                  completion_url='')
        for index, location in enumerate(locations):
            self.game_state.add_avatar(index, "", location)
        return self.turn_manager

    def construct_concurrent_turn_manager(self, avatars, locations):
        return self.construct_turn_manager(avatars, locations, ConcurrentTurnManager)

    def construct_sequential_turn_manager(self, avatars, locations):
        return self.construct_turn_manager(avatars, locations, SequentialTurnManager)

    def assert_at(self, avatar, location):
        self.assertEqual(avatar.location, location)
        cell = self.game_state.world_map.get_cell(location)
        self.assertEqual(cell.avatar, avatar)

    def get_avatar(self, player_id):
        return self.avatar_manager.get_avatar(player_id)

    def run_turn(self):
        self.turn_manager.run_turn()

    def run_by_manager_turn(self, construct_manager):
        '''
        Given:  > _
        (1)
        Expect: _ o
        '''
        construct_manager([MoveEastDummy], [ORIGIN])
        avatar = self.get_avatar(0)

        self.assert_at(avatar, ORIGIN)
        self.run_turn()
        self.assert_at(avatar, RIGHT_OF_ORIGIN)

    def run_by_manager_several_turns(self, construct_manager):
        '''
        Given:  > _ _ _ _ _
        (5)
        Expect: _ _ _ _ _ o
        '''
        construct_manager([MoveEastDummy], [ORIGIN])
        avatar = self.get_avatar(0)

        self.assertEqual(avatar.location, ORIGIN)
        [self.run_turn() for _ in range(5)]
        self.assertEqual(avatar.location, FIVE_RIGHT_OF_ORIGIN)

    def run_by_manager_several_turns_and_avatars(self, construct_manager):
        '''
        Given:  > _ _ _ _ _
                > _ _ _ _ _
        (5)
        Expect: _ _ _ _ _ o
                _ _ _ _ _ o
        '''
        construct_manager([MoveEastDummy, MoveEastDummy],
                                    [ORIGIN,        ABOVE_ORIGIN])
        avatar0 = self.get_avatar(0)
        avatar1 = self.get_avatar(1)

        self.assert_at(avatar0, ORIGIN)
        self.assert_at(avatar1, ABOVE_ORIGIN)
        [self.run_turn() for _ in range(5)]
        self.assert_at(avatar0, FIVE_RIGHT_OF_ORIGIN)
        self.assert_at(avatar1, FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE)

    def run_by_manager_move_chain_succeeds(self, construct_manager):
        '''
        Given:  > > > > > _

        Expect: _ o o o o o
        '''
        construct_manager([MoveEastDummy for _ in range(5)],
                                    [Location(x, 0) for x in range(5)])
        avatars = [self.get_avatar(i) for i in range(5)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(5)]
        self.run_turn()
        [self.assert_at(avatars[x], Location(x + 1, 0)) for x in range(5)]

    def run_by_manager_move_chain_fails_occupied(self, construct_manager):
        '''
        Given:  > > x _

        Expect: x x x _
        '''
        construct_manager([MoveEastDummy, MoveEastDummy, WaitDummy],
                                    [Location(x, 0) for x in range(3)])
        avatars = [self.get_avatar(i) for i in range(3)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]
        self.run_turn()
        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]

    def run_by_manager_move_chain_fails_collision(self, construct_manager):
        '''
        Given:  > > > _ <
        (1)
        Expect: x x x _ x
        '''
        locations = [Location(0, 0), Location(1, 0), Location(2, 0), Location(4, 0)]
        construct_manager(
            [MoveEastDummy, MoveEastDummy, MoveEastDummy, MoveWestDummy],
            locations)
        avatars = [self.get_avatar(i) for i in range(4)]

        [self.assert_at(avatars[i], locations[i]) for i in range(4)]
        self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(4)]

    def run_by_manager_move_chain_fails_cycle(self, construct_manager):
        '''
        Given:  > v
                ^ <
        (1)
        Expect: x x
                x x
        '''
        locations = [Location(0, 1), Location(1, 1), Location(1, 0), Location(0, 0)]
        construct_manager(
            [MoveEastDummy, MoveSouthDummy, MoveWestDummy, MoveNorthDummy],
            locations)
        avatars = [self.get_avatar(i) for i in range(4)]

        [self.assert_at(avatars[i], locations[i]) for i in range(4)]
        self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(4)]

    def run_by_manager_move_chain_fails_spiral(self, construct_manager):
        '''
        Given:  > > v
                  ^ <
        (1)
        Expect: x x x
                  x x
        '''
        locations = [Location(0, 1),
                     Location(1, 1),
                     Location(2, 1),
                     Location(2, 0),
                     Location(1, 0)]
        construct_manager(
            [MoveEastDummy, MoveEastDummy, MoveSouthDummy, MoveWestDummy, MoveNorthDummy],
            locations)
        avatars = [self.get_avatar(i) for i in range(5)]

        [self.assert_at(avatars[i], locations[i]) for i in range(5)]
        self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(5)]

    def build_test_by_constructor(self, constructor):
        self.run_by_manager_turn(constructor)
        self.run_by_manager_several_turns_and_avatars(constructor)
        self.run_by_manager_several_turns(constructor)
        self.run_by_manager_move_chain_fails_spiral(constructor)
        self.run_by_manager_move_chain_fails_cycle(constructor)
        self.run_by_manager_move_chain_fails_occupied(constructor)

    def test_concurrent_turn_manager(self):
        constructor = lambda x, y: self.construct_concurrent_turn_manager(x, y)
        self.build_test_by_constructor(constructor)
        self.run_by_manager_move_chain_fails_collision(constructor)
        self.run_by_manager_move_chain_succeeds(constructor)

    def sequential_move_chain_consecutive_avatars_fails(self):
        '''
        Given:  > > > > > _
        Expect: _ o o o o o

        This should fail for the sequential manager as the first avatar will bump into the second one
        '''
        self.construct_sequential_turn_manager([MoveEastDummy for _ in range(5)],
                          [Location(x, 0) for x in range(5)])
        avatars = [self.get_avatar(i) for i in range(5)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(5)]
        self.run_turn()
        [self.assert_at(avatars[x], Location(x, 0)) for x in range(4)]
        self.assert_at(avatars[4], Location(5, 0))

    def sequential_move_chain_fails_collision(self):
        '''
        Given:  > > > _ <
        (1)
        Expect: x x x _ x
        '''
        locations = [Location(0, 0), Location(1, 0), Location(2, 0), Location(4, 0)]
        self.construct_sequential_turn_manager(
            [MoveEastDummy, MoveEastDummy, MoveEastDummy, MoveWestDummy],
            locations)
        avatars = [self.get_avatar(i) for i in range(4)]

        [self.assert_at(avatars[i], locations[i]) for i in range(4)]
        self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in [0, 1, 3]]
        self.assert_at(avatars[2], Location(3, 0))

    def test_sequential_turn_manager(self):
        constructor = lambda x, y: self.construct_sequential_turn_manager(x, y)
        self.build_test_by_constructor(constructor)
        self.sequential_move_chain_consecutive_avatars_fails()
        self.sequential_move_chain_fails_collision()


if __name__ == '__main__':
    unittest.main()
