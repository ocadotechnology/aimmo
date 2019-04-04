from __future__ import absolute_import

import unittest
from json import dumps

from httmock import HTTMock

from game_manager import GameManager


class ConcreteGameManager(GameManager):
    def __init__(self, *args, **kwargs):
        self.clear()
        super(ConcreteGameManager, self).__init__(*args, **kwargs)

    def clear(self):
        self.final_games = set()
        self.removed_games = []
        self.added_games = {}

    def create_game(self, game_id, data):
        self.added_games[game_id] = data
        self.final_games.add(game_id)

    def delete_game(self, game_id):
        self.removed_games.append(game_id)
        try:
            self.final_games.remove(game_id)
        except KeyError:
            pass


class RequestMock(object):
    def __init__(self, num_games):
        self.value = self._generate_response(num_games)
        self.urls_requested = []

    def _generate_response(self, num_games):
        return {
            str(i): {
                "name": "Game {}".format(i),
                "settings": {"test": i, "test2": "Settings {}".format(i)},
            }
            for i in range(num_games)
        }

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)


class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.game_manager = ConcreteGameManager("http://test/")

    def test_correct_url_requested(self):
        mocker = RequestMock(0)
        with HTTMock(mocker):
            self.game_manager.update()
        self.assertEqual(len(mocker.urls_requested), 1)
        self.assertRegex(mocker.urls_requested[0], "http://test/*")

    def test_games_added(self):
        mocker = RequestMock(3)
        with HTTMock(mocker):
            self.game_manager.update()
        self.assertEqual(len(self.game_manager.final_games), 3)
        self.assertEqual(len(list(self.game_manager._data.get_games())), 3)
        for i in range(3):
            self.assertIn(str(i), self.game_manager.final_games)
            self.assertEqual(
                self.game_manager.added_games[str(i)]["settings"],
                {"test": i, "test2": "Settings {}".format(i)},
            )
            self.assertEqual(
                self.game_manager.added_games[str(i)]["name"], "Game {}".format(i)
            )

    def test_remove_games(self):
        mocker = RequestMock(3)
        with HTTMock(mocker):
            self.game_manager.update()
            del mocker.value["1"]
            self.game_manager.update()
        self.assertNotIn(1, self.game_manager.final_games)

    def test_added_games_given_correct_url(self):
        mocker = RequestMock(3)
        with HTTMock(mocker):
            self.game_manager.update()
        for i in range(3):
            self.assertEqual(
                self.game_manager.added_games[str(i)]["GAME_API_URL"],
                "http://test/{}/".format(i),
            )
            self.assertEqual(
                self.game_manager.added_games[str(i)]["name"], "Game {}".format(i)
            )
