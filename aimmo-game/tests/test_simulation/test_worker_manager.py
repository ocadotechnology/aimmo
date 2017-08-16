from __future__ import absolute_import

import unittest
from json import dumps

from httmock import HTTMock

from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_state import GameState
from simulation.worker_manager import WorkerManager
from .maps import InfiniteMap


class ConcreteWorkerManager(WorkerManager):
    def __init__(self, *args, **kwargs):
        self.final_workers = set()
        self.clear()
        super(ConcreteWorkerManager, self).__init__(*args, **kwargs)

    def clear(self):
        self.removed_workers = []
        self.added_workers = []

    def create_worker(self, player_id):
        self.added_workers.append(player_id)
        self.final_workers.add(player_id)

    def remove_worker(self, player_id):
        self.removed_workers.append(player_id)
        try:
            self.final_workers.remove(player_id)
        except KeyError:
            pass


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
                } for i in xrange(num_users)]
            }
        }

    def change_code(self, id, new_code):
        users = self.value['main']['users']
        for i in xrange(len(users)):
            if users[i]['id'] == id:
                users[i]['code'] = new_code

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)


class TestWorkerManager(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState(InfiniteMap(), AvatarManager())
        self.worker_manager = ConcreteWorkerManager(self.game_state, 'http://test')

    def test_correct_url(self):
        mocker = RequestMock(0)
        with HTTMock(mocker):
            self.worker_manager.update()
        self.assertEqual(len(mocker.urls_requested), 1)
        self.assertRegexpMatches(mocker.urls_requested[0], 'http://test/*')

    def test_workers_added(self):
        mocker = RequestMock(3)
        with HTTMock(mocker):
            self.worker_manager.update()
        self.assertEqual(len(self.worker_manager.final_workers), 3)
        for i in xrange(3):
            self.assertIn(i, self.game_state.avatar_manager.avatars_to_create_by_id)
            self.assertIn(i, self.worker_manager.final_workers)
            self.assertEqual(self.worker_manager.get_code(i), 'code for %s' % i)

    def test_changed_code(self):
        mocker = RequestMock(4)
        with HTTMock(mocker):
            self.worker_manager.update()
            mocker.change_code(0, 'changed 0')
            mocker.change_code(2, 'changed 2')
            self.worker_manager.update()

        for i in xrange(4):
            self.assertIn(i, self.worker_manager.final_workers)
            self.assertIn(i, self.game_state.avatar_manager.avatars_to_create_by_id)

        for i in (1, 3):
            self.assertEqual(self.worker_manager.get_code(i), 'code for %s' % i)
        for i in (0, 2):
            self.assertIn(i, self.worker_manager.added_workers)
            self.assertIn(i, self.worker_manager.removed_workers)
            self.assertEqual(self.worker_manager.get_code(i), 'changed %s' % i)

    def test_remove_avatars(self):
        mocker = RequestMock(3)
        with HTTMock(mocker):
            self.worker_manager.update()
            del mocker.value['main']['users'][1]
            self.worker_manager.update()
        self.assertNotIn(1, self.worker_manager.final_workers)
        self.assertNotIn(1, self.game_state.avatar_manager.avatars_to_delete_by_id)
