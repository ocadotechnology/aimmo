import random
import logging
from simulation.turn_manager import ConcurrentTurnManager
from simulation.game_state_provider import GameStateProvider
from simulation.logs_provider import LogsProvider
from simulation.map_generator import Main
from simulation.avatar.avatar_manager import AvatarManager
from .concrete_worker_manager import ConcreteWorkerManager
from .mock_communicator import MockCommunicator

LOGGER = logging.getLogger(__name__)


class FakeGameRunner(object):

    def __init__(self, settings=None, player_manager=None):
        # Default argument is now immutable
        if settings is None:
            settings = {'START_WIDTH': 3, 'START_HEIGHT': 3, 'OBSTACLE_RATIO': 0}

        self.settings = settings
        self.logs_provider = LogsProvider()
        self.state_provider = GameStateProvider()
        self.map_generator = Main(settings)
        if not player_manager:
            self.player_manager = AvatarManager()
        else:
            self.player_manager = player_manager
        self.mock_communicator = MockCommunicator()
        self.game_state = self.map_generator.get_game_state(self.player_manager)
        self.state_provider.set_world(self.game_state)
        self.worker_manager = ConcreteWorkerManager(game_state=self.game_state,
                                                    communicator=self.mock_communicator)
        self.turn_manager = ConcurrentTurnManager(game_state=self.game_state,
                                                  end_turn_callback=lambda: None,
                                                  communicator=self.mock_communicator,
                                                  state_provider=self.state_provider,
                                                  logs_provider=self.logs_provider)
        random.seed(0)

    def run_single_turn(self):
        self.worker_manager.update()
        self.turn_manager._run_single_turn()

    def get_logs(self, avatar_id):
        return self.logs_provider.get_user_logs(avatar_id)

    def get_avatar(self, avatar_id):
        return self.game_state.avatar_manager.get_avatar(avatar_id)

    def change_avatar_code(self, avatar_id, code):
        avatar = (user for user in self.mock_communicator.data["main"]["users"] if user["id"] == avatar_id).next()
        avatar["code"] = code
