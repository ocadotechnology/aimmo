from __future__ import absolute_import

from unittest import TestCase

from simulation.game_state import GameState
from simulation.location import Location

from .dummy_avatar import DummyAvatar, DummyAvatarManager
from .maps import AvatarMap, EmptyMap, InfiniteMap


class TestGameState(TestCase):
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

    def test_no_main_avatar_by_default(self):
        state = GameState(EmptyMap(), DummyAvatarManager())
        with self.assertRaises(KeyError):
            state.get_main_avatar()

    def test_get_main_avatar(self):
        (game_state, avatar, _, _) = self.game_state_with_two_avatars()
        game_state.main_avatar_id = avatar.player_id
        self.assertEqual(game_state.get_main_avatar(), avatar)
