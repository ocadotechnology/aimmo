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
    def setUp(self, map_type=InfiniteMap):
        self.world_map = map_type()
        self.av_manager = DummyAvatarManager()
        self.game_state = GameState(self.world_map, self.av_manager)

    def test_remove_non_existant_avatar(self):
        GameState(None, DummyAvatarManager()).remove_avatar(10)

    def test_remove_avatar(self):
        av_1 = DummyAvatar(1)
        av_1.location = Location(0, 0)
        av_2 = DummyAvatar(2)
        av_2.location = Location(1, 1)
        av_2.marked = True

        self.av_manager.add_avatar_directly(av_1)
        self.world_map.get_cell(Location(0, 0)).avatar = av_1
        self.av_manager.add_avatar_directly(av_2)
        self.world_map.get_cell(Location(1, 1)).avatar = av_2

        self.game_state.remove_avatar(1)

        self.assertNotIn(1, self.av_manager._avatars_by_id)
        self.assertEqual(self.world_map.get_cell((0, 0)).avatar, None)

        self.assertTrue(self.av_manager._avatars_by_id[2].marked)
        self.assertTrue(self.world_map.get_cell(Location(1, 1)).avatar.marked)

    def test_add_avatar(self):
        self.game_state.add_avatar(7, None, Location(10, 10))

        self.assertIn(7, self.av_manager._avatars_by_id)
        self.assertEqual(self.av_manager._avatars_by_id[7].location, Location(10, 10))

    def test_fog_of_war(self):
        game_state = GameState(InfiniteMap(), DummyAvatarManager())
        view = game_state.view(DummyAvatar(None), FogToEmpty())
        self.assertEqual(len(view['world_map']['cells']), 0)
        self.assertEqual(view['avatar_state'], 'Dummy')
