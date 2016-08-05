from __future__ import absolute_import
from .maps import InfiniteMap, AvatarMap, EmptyMap
from .dummy_avatar import DummyAvatarRunner
from .dummy_avatar import DummyAvatarManager
from simulation.game_state import GameState
from unittest import TestCase


class FogToEmpty(object):
    def apply_fog_of_war(self, map, wrapper):
        return EmptyMap()


class TestGameState(TestCase):
    def test_remove_non_existant_avatar(self):
        state = GameState(None, DummyAvatarManager([]))
        state.remove_avatar(10)

    def test_remove_avatar(self):
        map = InfiniteMap()
        manager = DummyAvatarManager([])

        avatar = DummyAvatarRunner((0, 0), 1)
        other_avatar = DummyAvatarRunner((0, 0), 2)
        other_avatar.marked = True
        manager.add_avatar_directly(avatar)
        manager.add_avatar_directly(other_avatar)

        state = GameState(map, manager)
        state.remove_avatar(1)

        self.assertTrue(manager.avatars_by_id[2].marked)
        self.assertNotIn(1, manager.avatars_by_id)
        self.assertEqual(map.get_cell((0, 0)).avatar, None)

    def test_add_avatar(self):
        state = GameState(AvatarMap(None), DummyAvatarManager([]))
        state.add_avatar(7, 'test')
        self.assertIn(7, state.avatar_manager.avatars_by_id)
        avatar = state.avatar_manager.avatars_by_id[7]
        self.assertEqual(avatar.location.x, 10)
        self.assertEqual(avatar.location.y, 10)

    def test_fog_of_war(self):
        state = GameState(InfiniteMap(), DummyAvatarManager([]))
        view = state.get_state_for(DummyAvatarRunner(None, None), FogToEmpty())
        self.assertEqual(len(view['world_map']['cells']), 0)
        self.assertEqual(view['avatar_state'], 'Dummy')
