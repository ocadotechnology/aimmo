from __future__ import absolute_import

from unittest import TestCase, skip

import service
from simulation.avatar.avatar_manager import AvatarManager
from simulation.geography.location import Location
from simulation.state.game_state import GameState
from simulation.state.world_state import WorldState
from simulation.turn_manager import state_provider
from simulation.world_map import WorldMap
from .test_simulation.dummy_avatar import MoveEastDummy
from .test_simulation.maps import MockPickup
from .test_simulation.test_world_map import MockCell


class SimpleAvatarManager(AvatarManager):
    def __init__(self):
        super(SimpleAvatarManager, self).__init__()

        avatar = MoveEastDummy(1, Location(0, -1))
        self.avatars_by_id[1] = avatar

class TestServiceAPI(TestCase):
    def setUp(self):
        service.app.config['TESTING'] = True
        self.app = service.app.test_client()

    def test_healthy(self):
        response = self.app.get('/')
        self.assertEqual(response.data, 'HEALTHY')

class TestServiceInternals(TestCase):
    def setUp(self):
        self.user_id = 1

    def setup_world(self):
        avatar_manager = SimpleAvatarManager()
        CELLS = [
            [
                {'pickup': MockPickup('b'), 'avatar': avatar_manager.avatars_by_id[1]},
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
                for y in range(3) for x in range(2)}
        state_provider.set_world(GameState(WorldMap(grid, {}), avatar_manager))

        world_state = WorldState(state_provider)
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

    @skip("not implemented")
    def test_pickup_list(self):
        result = self.setup_world()['map_features']['pickup']['create']
        pickup_pos_list = [(pickup['x'], pickup['y']) for pickup in result]
        self.assertIn((1, 1), pickup_pos_list)
        self.assertIn((0, -1), pickup_pos_list)
