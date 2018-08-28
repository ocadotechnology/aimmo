import random

from simulation import map_generator
from simulation.turn_manager import SequentialTurnManager
from simulation.logs import Logs
from tests.test_simulation.mock_communicator import MockCommunicator
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

    By default, the first avatar added to the world will be a MoveEastDummy.
    """
    def __init__(self, settings=SETTINGS, dummies_list=None, map_generator_class=map_generator.Main, logs=None):
        random.seed(0)
        if dummies_list is None:
            dummies_list = [MoveEastDummy]

        if logs is None:
            logs = Logs()

        self.generator = map_generator_class(settings)
        self.avatar_manager = DummyAvatarManager(dummies_list)
        self.game_state = self.generator.get_game_state(self.avatar_manager)
        self.turn_manager = SequentialTurnManager(game_state=self.game_state,
                                                  end_turn_callback=lambda: None,
                                                  communicator=MockCommunicator(),
                                                  logs=logs,
                                                  have_avatars_code_updated={})
