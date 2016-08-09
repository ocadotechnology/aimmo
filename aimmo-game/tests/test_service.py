from __future__ import absolute_import
import json
import service
from simulation.game_state import GameState
from simulation.location import Location
from .simulation.dummy_avatar import MoveEastDummy
from .simulation.test_world_map import MockCell
from simulation.turn_manager import state_provider
from simulation.world_map import WorldMap
from unittest import TestCase


class SimpleAvatarManager(object):
    avatars = [MoveEastDummy(1, Location(0, 1))]


class MockWorkerManager(object):
    def __init__(self, number_users=1):
        self.number_users = 1

    def get_code(self, id):
        if 0 < id <= self.number_users:
            return 'code_%s' % id
        raise KeyError

    def check_auth(self, id, auth_token):
        if 0 < id <= self.number_users:
            return auth_token == 'auth_%s' % id
        raise KeyError


class TestService(TestCase):
    @classmethod
    def setUpClass(cls):
        service.app.config['TESTING'] = True
        cls.app = service.app.test_client()
        cls.worker_manager = MockWorkerManager()
        service.worker_manager = cls.worker_manager

    def test_healthy(self):
        response = self.app.get('/')
        self.assertEqual(response.data, 'HEALTHY')

    def setup_world(self):
        CELLS = [
            [
                {},
                {'avatar': 'a'},
                {'generates_score': True},
            ],
            [
                {},
                {'habitable': False},
                {},
            ],
        ]
        grid = [[MockCell(Location(x, y), **CELLS[x][y])
                 for y in xrange(3)] for x in xrange(2)]
        state_provider.set_world(GameState(WorldMap(grid, {}), SimpleAvatarManager()))
        return service.get_world_state()

    def test_player_dict(self):
        player_dict = self.setup_world()['players']
        self.assertIn(1, player_dict)
        self.assertEqual(len(player_dict), 1)
        details = player_dict[1]
        self.assertEqual(details['id'], 1)
        self.assertEqual(details['x'], 0)
        self.assertEqual(details['y'], 1)
        self.assertEqual(details['health'], 5)
        self.assertEqual(details['score'], 0)

    def test_grid(self):
        result = self.setup_world()
        self.assertEqual(result['score_locations'], [(0, 2)])
        self.assertEqual(result['width'], 2)
        self.assertEqual(result['height'], 3)
        self.assertEqual(result['layout'], [[0, 0, 2], [0, 1, 0]])

    def test_get_player_data_success(self):
        response = self.app.get('/player/1?auth_token=auth_1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['code'], 'code_1')

    def test_get_player_data_for_non_existant_player(self):
        response = self.app.get('/player/5?auth_token=auth_5')
        self.assertEqual(response.status_code, 404)

    def test_get_player_data_invlaid_auth_token(self):
        response = self.app.get('/player/1?auth_token=auth_5')
        self.assertEqual(response.status_code, 404)
