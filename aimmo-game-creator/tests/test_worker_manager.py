from __future__ import absolute_import
import cPickle as pickle
from httmock import HTTMock
from json import dumps
from worker_manager import WorkerManager
import unittest


class ConcreteWorkerManager(WorkerManager):
    def __init__(self, *args, **kwargs):
        self.final_workers = set()
        self.clear()
        super(ConcreteWorkerManager, self).__init__(*args, **kwargs)

    def clear(self):
        self.removed_workers = []
        self.added_workers = {}

    def create_worker(self, game_id, data):
        self.added_workers[game_id] = data
        self.final_workers.add(game_id)

    def remove_worker(self, game_id):
        self.removed_workers.append(game_id)
        try:
            self.final_workers.remove(game_id)
        except KeyError:
            pass


class RequestMock(object):
    def __init__(self, num_games):
        self.value = self._generate_response(num_games)
        self.urls_requested = []

    def _generate_response(self, num_games):
        return {
            str(i): {
                'name': 'Game %s' % i,
                'settings': pickle.dumps({
                    'test': i,
                    'test2': 'Settings %s' % i,
                }),
                'auth_token': 'auth_%s' % i,
            } for i in xrange(num_games)
        }

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)


class TestWorkerManager(unittest.TestCase):
    def setUp(self):
        self.worker_manager = ConcreteWorkerManager('http://test/', 'auth')

    def test_correct_url_requested(self):
        mocker = RequestMock(0)
        with HTTMock(mocker):
            self.worker_manager.update()
        self.assertEqual(len(mocker.urls_requested), 1)
        self.assertEqual(mocker.urls_requested[0], 'http://test/?auth_token=auth')

    def test_workers_added(self):
        mocker = RequestMock(3)
        with HTTMock(mocker):
            self.worker_manager.update()
        self.assertEqual(len(self.worker_manager.final_workers), 3)
        self.assertEqual(len(list(self.worker_manager._data.get_games())), 3)
        for i in xrange(3):
            self.assertIn(str(i), self.worker_manager.final_workers)
            self.assertEqual(
                pickle.loads(str(self.worker_manager.added_workers[str(i)]['settings'])),
                {'test': i, 'test2': 'Settings %s' % i}
            )
            self.assertEqual(self.worker_manager.added_workers[str(i)]['name'], 'Game %s' % i)
            self.assertEqual(self.worker_manager.added_workers[str(i)]['auth_token'], 'auth_%s' % i)

    def test_remove_games(self):
        mocker = RequestMock(3)
        with HTTMock(mocker):
            self.worker_manager.update()
            del mocker.value['1']
            self.worker_manager.update()
        self.assertNotIn(1, self.worker_manager.final_workers)

    def test_added_workers_given_correct_url(self):
        mocker = RequestMock(3)
        with HTTMock(mocker):
            self.worker_manager.update()
        for i in xrange(3):
            self.assertEqual(
                self.worker_manager.added_workers[str(i)]['GAME_API_URL'],
                'http://test/{}/'.format(i)
            )
            self.assertEqual(self.worker_manager.added_workers[str(i)]['name'], 'Game %s' % i)
