from unittest import TestCase
from json import dumps

import mock

from .mock_communicator import MockCommunicator
from .maps import InfiniteMap
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_state import GameState
from simulation.game_runner import GameRunner
from .concrete_worker_manager import ConcreteWorkerManager


class RequestMock(object):
    def __init__(self, num_users):
        self.value = self._generate_response(num_users)
        self.urls_requested = []

    def _generate_response(self, num_users):
        return {
            'main': {
                'parameters': [],
                'main_avatar': None,
                'users': [{
                    'id': i,
                    'code': 'code for %s' % i,
                } for i in range(num_users)]
            }
        }

    def change_code(self, id, new_code):
        users = self.value['main']['users']
        for i in range(len(users)):
            if users[i]['id'] == id:
                users[i]['code'] = new_code

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)


class TestGameRunner(TestCase):
    def setUp(self):
        self.mock_communicator = MockCommunicator()
        game_state = GameState(InfiniteMap(), AvatarManager())
        self.game_runner = GameRunner(communicator=self.mock_communicator,
                                      worker_manager=ConcreteWorkerManager(),
                                      game_state=game_state)

    def test_correct_url(self):
        self.mock_communicator.get_game_metadata = mock.MagicMock()
        self.game_runner.update()
        # noinspection PyUnresolvedReferences
        self.mock_communicator.get_game_metadata.assert_called_once()

    def test_workers_and_avatars_added(self):
        self.mock_communicator.data = RequestMock(3).value
        self.game_runner.update()
        self.assertEqual(len(self.game_runner.worker_manager.final_workers), 3)
        for i in range(3):
            self.assertIn(i, self.game_runner.game_state.avatar_manager.avatars_by_id)
            self.assertIn(i, self.game_runner.worker_manager.final_workers)
            self.assertEqual(self.game_runner.worker_manager.get_code(i), 'code for %s' % i)

    def test_changed_code(self):
        self.mock_communicator.data = RequestMock(4).value
        self.game_runner.update()
        self.mock_communicator.change_code(0, 'changed 0')
        self.mock_communicator.change_code(2, 'changed 2')
        self.game_runner.update()

        for i in range(4):
            self.assertIn(i, self.game_runner.worker_manager.final_workers)
            self.assertIn(i, self.game_runner.game_state.avatar_manager.avatars_by_id)

        for i in (1, 3):
            self.assertEqual(self.game_runner.worker_manager.get_code(i), 'code for %s' % i)

        for i in (0, 2):
            self.assertIn(i, self.game_runner.worker_manager.updated_workers)
            self.assertEqual(self.game_runner.worker_manager.get_code(i), 'changed %s' % i)

    def test_remove_avatars(self):
        self.mock_communicator.data = RequestMock(3).value
        self.game_runner.update()
        del self.mock_communicator.data['main']['users'][1]
        self.game_runner.update()

        for i in range(3):
            if i == 1:
                self.assertNotIn(i, self.game_runner.worker_manager.final_workers)
                self.assertNotIn(i, self.game_runner.game_state.avatar_manager.avatars_by_id)
            else:
                self.assertIn(i, self.game_runner.worker_manager.final_workers)
                self.assertIn(i, self.game_runner.game_state.avatar_manager.avatars_by_id)
