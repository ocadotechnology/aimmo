from __future__ import absolute_import
import service
from simulation.game_state import GameState
from simulation.location import Location
from .simulation.dummy_avatar import DummyAvatarRunner
from .simulation.test_world_map import MockCell
from simulation.turn_manager import state_provider
from simulation.world_map import WorldMap
from unittest import TestCase


class SimpleAvatarManager(object):
    avatars = [DummyAvatarRunner(Location(0, 1), 1)]


class TestService(TestCase):
    def test_healthy(self):
        service.app.config['TESTING'] = True
        self.app = service.app.test_client()
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
        state_provider.set_world(GameState(WorldMap(grid), SimpleAvatarManager()))
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
