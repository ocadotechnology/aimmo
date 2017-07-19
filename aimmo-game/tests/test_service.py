from __future__ import absolute_import

from unittest import TestCase

from simulation.game_state import GameState
from simulation.location import Location
from simulation.turn_manager import state_provider
from simulation.world_map import WorldMap
from simulation.world_state import WorldState

from .test_simulation.dummy_avatar import MoveEastDummy
from .test_simulation.maps import MockPickup
from .test_simulation.test_world_map import MockCell


class SimpleAvatarManager(object):
    avatars = [MoveEastDummy(1, Location(0, -1))]


class TestService(TestCase):
    def test_healthy(self):
        service.app.config['TESTING'] = True
        self.app = service.app.test_client()
        response = self.app.get('/')
        self.assertEqual(response.data, 'HEALTHY')

    def setup_world(self):
        avatar_manager = SimpleAvatarManager()
        CELLS = [
            [
                {'pickup': MockPickup('b'), 'avatar': avatar_manager.avatars[0]},
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
        return WorldState.get_world_state()

    def test_player_dict(self):
        player_dict = self.setup_world()['players']
        self.assertIn(1, player_dict)
        self.assertEqual(len(player_dict), 1)
        details = player_dict[1]
        self.assertEqual(details['id'], 1)
        self.assertEqual(details['x'], 0)
        self.assertEqual(details['y'], -1)
        self.assertEqual(details['health'], 5)
        self.assertEqual(details['score'], 0)

    def test_score_locations(self):
        result = self.setup_world()
        self.assertEqual(result['score_locations'], [(0, 1)])

    def test_width(self):
        result = self.setup_world()
        self.assertEqual(result['width'], 2)

    def test_height(self):
        result = self.setup_world()
        self.assertEqual(result['height'], 3)

    def test_layout(self):
        result = self.setup_world()
        expected = {
            0: {
                -1: 0,
                0: 0,
                1: 2,
            },
            1: {
                -1: 0,
                0: 1,
                1: 0,
            }
        }
        self.assertEqual(result['layout'], expected)

    def test_min_x(self):
        result = self.setup_world()
        self.assertEqual(result['minX'], 0)

    def test_min_y(self):
        result = self.setup_world()
        self.assertEqual(result['minY'], -1)

    def test_max_x(self):
        result = self.setup_world()
        self.assertEqual(result['maxX'], 1)

    def test_max_y(self):
        result = self.setup_world()
        self.assertEqual(result['maxY'], 1)

    def test_pickup_list(self):
        result = self.setup_world()
        self.assertIn({'name': 'a', 'location': (1, 1)}, result['pickups'])
        self.assertIn({'name': 'b', 'location': (0, -1)}, result['pickups'])
