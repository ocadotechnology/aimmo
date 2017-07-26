from __future__ import absolute_import

from unittest import TestCase

from simulation.game_state import GameState
from simulation.location import Location
from simulation.turn_manager import state_provider
from simulation.world_map import WorldMap
from simulation.world_state import WorldState
from simulation.avatar.avatar_manager import AvatarManager

import service

from .test_simulation.dummy_avatar import MoveEastDummy
from .test_simulation.maps import MockPickup
from .test_simulation.test_world_map import MockCell

class SimpleAvatarManager(AvatarManager):
    def __init__(self):
        avatar = MoveEastDummy(1, Location(0, -1))
        self.avatars_by_id = {
            1 : avatar
        }

class TestService(TestCase):
    def setUp(self):
        self.user_id = 1

    def test_healthy(self):
        service.app.config['TESTING'] = True
        self.app = service.app.test_client()
        response = self.app.get('/')
        self.assertEqual(response.data, 'HEALTHY')

    def setup_world(self):
        avatar_manager = SimpleAvatarManager()
        CELLS = [
            [
                {'pickup': MockPickup('b'), 'avatar': avatar_manager.get_avatar(self.user_id)},
                {},
                {'generates_score': True},
            ],
            [
                {},
                {'habitable': False},
                {'pickup': MockPickup('a')},
            ],
        ]
        grid = {Location(x, y-1): MockCell(Location(x, y-1), **CELLS[x][y])
                for y in xrange(3) for x in xrange(2)}
        state_provider.set_world(GameState(WorldMap(grid, {}), avatar_manager))

        world_state = WorldState(state_provider, self.user_id)
        world_state.ready_to_update = True

        return world_state.get_updates()

    def test_player_dict(self):
        player_list = self.setup_world()['players']['create']
        self.assertEqual(len(player_list), 1)
        details = player_list[0]
        self.assertEqual(details['id'], 1)
        self.assertEqual(details['x'], 0)
        self.assertEqual(details['y'], -1)
        self.assertEqual(details['health'], 5)
        self.assertEqual(details['score'], 0)

    def test_score_locations(self):
        result = self.setup_world()['map_features']['score_point']['create']
        self.assertEqual(result[0]['x'], 0)
        self.assertEqual(result[0]['y'], 1)

    def test_pickup_list(self):
        result = self.setup_world()['map_features']['pickup']['create']
        pickup_pos_list = [(pickup['x'], pickup['y']) for pickup in result]
        self.assertIn((1, 1), pickup_pos_list)
        self.assertIn((0, -1), pickup_pos_list)
