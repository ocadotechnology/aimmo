import unittest
import random
from simulation.communicator import Communicator
# from simulation.worker_manager import LocalWorkerManager
# from simulation.turn_manager import ConcurrentTurnManager
# from simulation.map_generator import Main
# from simulation.avatar.avatar_manager import AvatarManager
# from .test_worker_manager import ConcreteWorkerManager

class MockCommunicator(Communicator):
    def __init__(self):
        pass

    def get_game_metadata(self):
        data = {
            "main": {
                "parameters": [],
                "main_avatar": 1,
                "users": [
                    {
                        "id": 1,
                        "code": "class Avatar..."
                    }
                ]
            }
        }
        return data

    def mark_game_complete(self, data=None):
        return {}


class TestAvatarLocation(unittest.TestCase):

    def test_wait_action(self):
        pass
        # settings = {'START_WIDTH': 3, 'START_HEIGHT': 3, 'OBSTACLE_RATIO': 0}
        # map_generator = Main(settings)
        # player_manager = AvatarManager()
        # communicator = MockCommunicator()
        # game_state = map_generator.get_game_state(player_manager)
        # worker_manager = ConcreteWorkerManager(game_state=game_state,communicator=communicator)
        # turn_manager = ConcurrentTurnManager(game_state=game_state, end_turn_callback = lambda: None,communicator=communicator)
        # random.seed(0)
        # worker_manager.update()
        # turn_manager._run_single_turn()











































