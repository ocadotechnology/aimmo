from __future__ import absolute_import

from unittest import TestCase

from simulation.game_state import GameState
from simulation.location import Location
from .dummy_avatar import DummyAvatar
from .dummy_avatar import DummyAvatarManager
from .maps import InfiniteMap, AvatarMap, EmptyMap


class TestGameState(TestCase):
    def test_remove_non_existant_avatar(self):
        state = GameState(None, DummyAvatarManager())
        state.remove_avatar(10)

    def test_remove_avatar(self):
        world_map = InfiniteMap()
        manager = DummyAvatarManager()
        game_state = GameState(world_map, manager)

        avatar1 = DummyAvatar(1, Location(0, 0))
        avatar2 = DummyAvatar(2, Location(1, 1))
        avatar2.marked = True

        manager.add_avatar_directly(avatar1)
        world_map.get_cell(Location(0, 0)).avatar = avatar1
        manager.add_avatar_directly(avatar2)
        world_map.get_cell(Location(1, 1)).avatar = avatar2

        game_state.remove_avatar(1)

        self.assertNotIn(1, manager.avatars_by_id)
        self.assertEqual(world_map.get_cell(Location(0, 0)).avatar, None)

        self.assertTrue(manager.avatars_by_id[2].marked)
        self.assertTrue(world_map.get_cell(Location(1, 1)).avatar.marked)

    def game_state_with_two_avatars(self, world_map=None, avatar_manager=None):
        if world_map is None:
            world_map = EmptyMap()
        if avatar_manager is None:
            avatar_manager = DummyAvatarManager()

        avatar = DummyAvatar(1, (0, 0))
        other_avatar = DummyAvatar(2, (0, 0))
        other_avatar.marked = True
        avatar_manager.avatars_by_id[1] = avatar
        avatar_manager.avatars_by_id[2] = other_avatar
        game_state = GameState(world_map, avatar_manager)

        return (game_state, avatar, world_map, avatar_manager)

    def test_add_avatar(self):
        state = GameState(AvatarMap(None), DummyAvatarManager())
        state.add_avatar(7)
        self.assertIn(7, state.avatar_manager.avatars_by_id)
        avatar = state.avatar_manager.avatars_by_id[7]
        self.assertEqual(avatar.location.x, 10)
        self.assertEqual(avatar.location.y, 10)

    def test_updates_map(self):
        map = InfiniteMap()
        state = GameState(map, DummyAvatarManager())
        state.update_environment()
        self.assertEqual(map.updates, 1)

    def test_updates_map_with_correct_num_avatars(self):
        map = InfiniteMap()
        manager = DummyAvatarManager()
        manager.add_avatar(1)
        state = GameState(map, manager)
        state.update_environment()
        self.assertEqual(map.num_avatars, 1)
        manager.add_avatar(2)
        manager.add_avatar(3)
        state.update_environment()
        self.assertEqual(map.num_avatars, 3)

    def test_no_main_avatar_by_default(self):
        state = GameState(EmptyMap(), DummyAvatarManager())
        with self.assertRaises(KeyError):
            state.get_main_avatar()

    def test_get_main_avatar(self):
        (game_state, avatar, _, _) = self.game_state_with_two_avatars()
        game_state.main_avatar_id = avatar.player_id
        self.assertEqual(game_state.get_main_avatar(), avatar)

    def test_is_complete_calls_lambda(self):
        class LambdaTest(object):
            def __init__(self, return_value):
                self.return_value = return_value

            def __call__(self, game_state):
                self.game_state = game_state
                return self.return_value

        test = LambdaTest(True)
        game_state = GameState(EmptyMap(), DummyAvatarManager(), test)
        self.assertTrue(game_state.is_complete())
        test.return_value = False
        self.assertFalse(game_state.is_complete())
