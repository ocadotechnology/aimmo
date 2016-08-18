from __future__ import absolute_import

from unittest import TestCase

from simulation.game_state import GameState
from simulation.location import Location

from .maps import InfiniteMap, AvatarMap, EmptyMap
from .dummy_avatar import DummyAvatar
from .dummy_avatar import DummyAvatarManager


class FogToEmpty(object):
    def apply_fog_of_war(self, map, wrapper):
        return EmptyMap()


class TestGameState(TestCase):
    def test_remove_non_existant_avatar(self):
        game_state = GameState(None, DummyAvatarManager())
        with game_state:
            game_state.remove_avatar(10)

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

        with game_state:
            game_state.remove_avatar(1)

        self.assertNotIn(1, manager.avatars_by_id)
        self.assertEqual(world_map.get_cell((0, 0)).avatar, None)

        self.assertTrue(manager.avatars_by_id[2].marked)
        self.assertTrue(world_map.get_cell(Location(1, 1)).avatar.marked)

    def test_add_avatar(self):
        game_state = GameState(AvatarMap(None), DummyAvatarManager())

        with game_state:
            game_state.add_avatar(7, "")

        self.assertIn(7, game_state.avatar_manager.avatars_by_id)
        avatar = game_state.avatar_manager.avatars_by_id[7]
        self.assertEqual(avatar.location.x, 10)
        self.assertEqual(avatar.location.y, 10)

    def test_fog_of_war(self):
        game_state = GameState(InfiniteMap(), DummyAvatarManager())
        view = game_state.get_state_for(DummyAvatar(None, None), FogToEmpty())
        self.assertEqual(len(view['world_map']['cells']), 0)
        self.assertEqual(view['avatar_state'], 'Dummy')
