import random
from unittest import TestCase

from tests.test_simulation.dummy_avatar import DummyAvatarManager, MoveEastDummy
from tests.test_simulation.dummy_avatar import MoveEastDummy

from simulation import map_generator
from simulation.turn_manager import SequentialTurnManager
from simulation.location import Location
from simulation.pickups import HealthPickup


SETTINGS = {
    'START_HEIGHT': 5,
    'START_WIDTH': 5,
    'OBSTACLE_RATIO': 0,
}


class TestGame(object):
    def __init__(self, settings=SETTINGS):
        random.seed(0)
        self.generator = map_generator.Main(settings)
        self.avatar_manager = DummyAvatarManager([MoveEastDummy])
        self.game_state = self.generator.get_game_state(self.avatar_manager)
        self.turn_manager = SequentialTurnManager(game_state=self.game_state, end_turn_callback=lambda: None,
                                                  completion_url='')


class TestHealthPickupAndEffects(TestCase):
    def test_health_pickups_and_effects_apply(self):
        game = TestGame()
        game.game_state.add_avatar(1, None, Location(0, 0))
        cell = game.game_state.world_map.get_cell(Location(0, 0))
        self.assertEqual(cell.avatar, game.avatar_manager.get_avatar(1))
        self.assertEqual(cell.avatar.health, 5)

        cell = game.game_state.world_map.get_cell(Location(1, 0))
        cell.pickup = HealthPickup(cell)

        game.turn_manager._run_single_turn()

        self.assertEqual(cell.avatar, game.avatar_manager.get_avatar(1))
        self.assertEqual(cell.avatar.health, 8)
