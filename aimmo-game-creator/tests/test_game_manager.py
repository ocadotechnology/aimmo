from __future__ import absolute_import

import unittest
from json import dumps

from game_manager import TOKEN_MAX_LENGTH, GameManager, KubernetesGameManager
from httmock import HTTMock
from unittest.mock import MagicMock, call


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
                "status": "r",
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

    def test_token_generation(self):
        token = self.game_manager._generate_game_token()
        self.assertTrue(isinstance(token, str))
        self.assertLessEqual(len(token), TOKEN_MAX_LENGTH)

    def test_adding_a_game_creates_game_allocation(self):
        game_manager = KubernetesGameManager("http://test/*")
        custom_objects_api = MagicMock()
        custom_objects_api.list_namespaced_custom_object = MagicMock(
            return_value={"items": [{"metadata": {"name": "test"}}]}
        )
        game_manager.custom_objects_api = custom_objects_api
        game_manager.secret_creator = MagicMock()
        game_manager.api = MagicMock()
        game_manager.networking_api = MagicMock()
        game_manager.create_game(1, {"worksheet_id": 1})

        custom_objects_api.create_namespaced_custom_object.assert_called_with(
            group="allocation.agones.dev",
            version="v1",
            namespace="default",
            plural="gameserverallocations",
            body={
                "apiVersion": "allocation.agones.dev/v1",
                "kind": "GameServerAllocation",
                "metadata": {"generateName": "game-allocation-"},
                "spec": {
                    "required": {"matchLabels": {"agones.dev/fleet": "aimmo-game"}},
                    "scheduling": "Packed",
                    "metadata": {
                        "labels": {"game-id": 1},
                        "annotations": {
                            "worksheet_id": 1,
                        },
                    },
                },
            },
        )

    def test_delete_game(self):
        game_manager = KubernetesGameManager("http://test/*")
        custom_objects_api = MagicMock()
        custom_objects_api.list_namespaced_custom_object.return_value = {
            "items": [{"metadata": {"name": "aimmo-game-100-test"}}]
        }
        game_manager.custom_objects_api = custom_objects_api
        game_manager.secret_creator = MagicMock()
        game_manager.api = MagicMock()
        game_manager.networking_api = MagicMock()

        game_manager.delete_game(100)

        custom_objects_api.assert_has_calls(
            [
                call.list_namespaced_custom_object(
                    group="agones.dev",
                    version="v1",
                    namespace="default",
                    plural="gameservers",
                    label_selector="game-id=100",
                ),
                call.delete_namespaced_custom_object(
                    group="agones.dev",
                    version="v1",
                    namespace="default",
                    plural="gameservers",
                    name="aimmo-game-100-test",
                ),
            ]
        )

        # Test again with no ingress
        game_manager.networking_api.list_namespaced_ingress.return_value.items = []
        game_manager.delete_game(100)
