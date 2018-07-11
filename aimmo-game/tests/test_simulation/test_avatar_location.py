import unittest
import random
from simulation.communicator import Communicator
from simulation.worker_manager import WorkerManager
from simulation.turn_manager import ConcurrentTurnManager
from simulation.map_generator import Main
from simulation.avatar.avatar_manager import AvatarManager
from .concrete_worker_manager import ConcreteWorkerManager


class MockCommunicator(Communicator):
    def __init__(self):
        self.data = {
            "main": {
                "parameters": [],
                "main_avatar": 1,
                "users": [
                    {
                        "id": 1,
                        "code": "class Avatar:"
                    }
                ]
            }
        }
        pass

    def get_game_metadata(self):
        return self.data

    def mark_game_complete(self, data=None):
        return {}


class FakeGameRunner():

    def __init__(self, settings={'START_WIDTH': 3, 'START_HEIGHT': 3, 'OBSTACLE_RATIO': 0}):
        self.settings = settings
        self.map_generator = Main(settings)
        self.player_manager = AvatarManager()
        self.mock_communicator = MockCommunicator()
        self.game_state = self.map_generator.get_game_state(self.player_manager)
        self.worker_manager = ConcreteWorkerManager(game_state=self.game_state, communicator=self.mock_communicator)
        self.turn_manager = ConcurrentTurnManager(game_state=self.game_state, end_turn_callback=lambda: None,
                                                  communicator=self.mock_communicator)
        random.seed(0)

    def run_single_turn(self):
        self.worker_manager.update()
        self.turn_manager._run_single_turn()

    def get_avatar(self, avatar_id):
        return self.game_state.avatar_manager.get_avatar(avatar_id)

    def change_avatar_code(self, avatar_id, code):
        avatar = (user for user in self.mock_communicator.data["main"]["users"] if user["id"] == avatar_id).next()
        avatar["code"] = code


class TestAvatarLocation(unittest.TestCase):

    def test_avatar_location_stays_same_after_code_change(self):
        game_runner = FakeGameRunner()
        game_runner.run_single_turn()
        avatar_location_before_code_change = game_runner.get_avatar(1).location
        game_runner.change_avatar_code(1, "class Avatar: different code")
        game_runner.run_single_turn()
        avatar_location_after_code_change = game_runner.get_avatar(1).location
        self.assertEqual(avatar_location_before_code_change, avatar_location_after_code_change)


