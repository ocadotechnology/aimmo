import random
import logging

from simulation.turn_manager import ConcurrentTurnManager
from simulation.map_generator import Main
from simulation.logs import Logs
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_runner import GameRunner
from .concrete_worker_manager import ConcreteWorkerManager
from .mock_communicator import MockCommunicator

LOGGER = logging.getLogger(__name__)


class FakeGameRunner(object):
    def __init__(self, settings=None, player_manager=None):
        # Default argument is now immutable
        if settings is None:
            settings = {'START_WIDTH': 3, 'START_HEIGHT': 3, 'OBSTACLE_RATIO': 0}

        self.settings = settings
        self.logs = Logs()
        self.map_generator = Main(settings)
        if not player_manager:
            self.player_manager = AvatarManager()
        else:
            self.player_manager = player_manager
        self.mock_communicator = MockCommunicator()

        game_state = self.map_generator.get_game_state(self.player_manager)
        worker_manager = ConcreteWorkerManager()
        self.game_runner = GameRunner(worker_manager=worker_manager,
                                      game_state=game_state,
                                      communicator=self.mock_communicator)
        self.turn_manager = ConcurrentTurnManager(game_state=self.game_runner.game_state,
                                                  end_turn_callback=lambda: None,
                                                  communicator=self.mock_communicator,
                                                  logs=self.logs,
                                                  have_avatars_code_updated={})
        random.seed(0)

    def run_single_turn(self):
        self.game_runner.update()
        self.turn_manager._run_single_turn()

    def get_logs(self, avatar_id):
        return self.logs.get_user_logs(avatar_id)

    def get_avatar(self, avatar_id):
        return self.game_runner.game_state.avatar_manager.get_avatar(avatar_id)

    def change_avatar_code(self, avatar_id, code):
        avatar = (user for user in self.mock_communicator.data["main"]["users"] if user["id"] == avatar_id).next()
        avatar["code"] = code
