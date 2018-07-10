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


class TestAvatarLocation(unittest.TestCase):

    def test_wait_action(self):
        settings = {'START_WIDTH': 3, 'START_HEIGHT': 3, 'OBSTACLE_RATIO': 0}
        map_generator = Main(settings)
        player_manager = AvatarManager()
        mock_communicator = MockCommunicator()
        game_state = map_generator.get_game_state(player_manager)
        worker_manager = ConcreteWorkerManager(game_state=game_state, communicator=mock_communicator)
        turn_manager = ConcurrentTurnManager(game_state=game_state, end_turn_callback = lambda: None, communicator=mock_communicator)
        random.seed(0)
        worker_manager.update()
        turn_manager._run_single_turn()
        state_before_code_change = game_state.get_state_for(game_state.avatar_manager.active_avatars[0])
        mock_communicator.data["main"]["users"][0]["code"] = "class Avatar: different code"
        worker_manager.update()
        turn_manager._run_single_turn()
        state_after_code_change = game_state.get_state_for(game_state.avatar_manager.active_avatars[0])
        self.assertEqual(state_before_code_change, state_after_code_change)











































