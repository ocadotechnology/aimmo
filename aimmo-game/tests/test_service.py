from __future__ import absolute_import

from unittest import TestCase

from simulation.game_state import GameState
from simulation.location import Location
from simulation.turn_manager import state_provider
from simulation.world_map import WorldMap
from simulation.world_state import WorldState

import service

from .test_simulation.dummy_avatar import MoveEastDummy
from .test_simulation.maps import MockPickup
from .test_simulation.test_world_map import MockCell

class SimpleAvatarManager(object):
    avatars = [MoveEastDummy(1, Location(0, -1))]

# TODO: Write test for the new API...
class TestService(TestCase):
    def test_healthy(self):
        service.app.config['TESTING'] = True
        self.app = service.app.test_client()
        response = self.app.get('/')
        self.assertEqual(response.data, 'HEALTHY')
