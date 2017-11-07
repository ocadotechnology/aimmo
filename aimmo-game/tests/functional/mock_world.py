import random

from simulation import map_generator
from simulation.turn_manager import SequentialTurnManager

from tests.test_simulation.dummy_avatar import DummyAvatarManager, MoveEastDummy

SETTINGS = {
    'START_HEIGHT': 5,
    'START_WIDTH': 5,
    'OBSTACLE_RATIO': 0,
}


class MockWorld(object):
    """
    Creates an object that mocks the whole game and can be used in various testing.
    It holds the map generator, avatar manager, game state and turn manager. Takes settings as a parameter,
    if defaults are unsuitable.
    """
    def __init__(self, settings=SETTINGS):
        random.seed(0)
        self.generator = map_generator.Main(settings)
        self.avatar_manager = DummyAvatarManager([MoveEastDummy])
        self.game_state = self.generator.get_game_state(self.avatar_manager)
        self.turn_manager = SequentialTurnManager(game_state=self.game_state, end_turn_callback=lambda: None,
                                                  completion_url='')
