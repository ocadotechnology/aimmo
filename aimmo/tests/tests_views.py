import ast
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from aimmo import models, app_settings

app_settings.GAME_SERVER_URL_FUNCTION = lambda game_id: (
    "base %s" % game_id,
    "path %s" % game_id,
)
app_settings.GAME_SERVER_PORT_FUNCTION = lambda game_id: 0
app_settings.GAME_SERVER_SSL_FLAG = True


class TestViews(TestCase):
    CODE = "class Avatar: pass"

    EXPECTED_GAMES = {
        "main": {
            "parameters": [],
            "main_avatar": 1,
            "users": [
                {"id": 1, "code": CODE},
                {"id": 2, "code": "test2"},
                {"id": 3, "code": "test3"},
            ],
        }
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("test", "test@example.com", "password")
        cls.user.is_staff = True
        cls.user.save()
        cls.game = models.Game(id=1, name="test", public=True)
        cls.game.save()

    def setUp(self):
        self.game.refresh_from_db()

    def login(self):
        c = Client()
        c.login(username="test", password="password")
        return c

    def _go_to_page(self, link, kwarg_name, game_id):
        c = Client()
        response = c.get(reverse(link, kwargs={kwarg_name: game_id}))
        return response

    def _make_game_private(self):
        self.game.public = False
        self.game.save()

    def test_add_new_code(self):
        c = self.login()
        response = c.post(reverse("aimmo/code", kwargs={"id": 1}), {"code": self.CODE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            models.Avatar.objects.get(owner__username="test").code, self.CODE
        )

    def test_update_code(self):
        c = self.login()
        models.Avatar(owner=self.user, code="test", game=self.game).save()
        response = c.post(reverse("aimmo/code", kwargs={"id": 1}), {"code": self.CODE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            models.Avatar.objects.get(owner__username="test").code, self.CODE
        )

    def test_code_for_non_existant_game(self):
        c = self.login()
        response = c.post(reverse("aimmo/code", kwargs={"id": 2}), {"code": self.CODE})
        self.assertEqual(response.status_code, 404)

    def test_code_for_non_authed_user(self):
        self.game.public = False
        self.game.save()
        c = self.login()
        response = c.post(reverse("aimmo/code", kwargs={"id": 1}), {"code": self.CODE})
        self.assertEqual(response.status_code, 404)

    def test_default_code(self):
        c = self.login()
        response = c.get(reverse("aimmo/code", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)["code"].startswith("class Avatar"))

    def test_retrieve_code(self):
        models.Avatar(owner=self.user, code=self.CODE, game=self.game).save()
        c = self.login()
        response = c.get(reverse("aimmo/code", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"code": self.CODE})

    def _associate_game_as_level_num(self, level_num=1, user=None, game=None):
        if game is None:
            game = self.game
        if user is None:
            user = self.user
        models.LevelAttempt(user=user, game=game, level_number=level_num).save()
        models.Game(name="Wrong").save()

    def test_play(self):
        c = self.login()
        response = c.get(reverse("aimmo/play", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["current_user_player_key"], self.user.pk)
        self.assertEqual(response.context["game_url_base"], "base 1")
        self.assertEqual(response.context["game_url_path"], "path 1")

    def test_play_for_non_existent_game(self):
        c = self.login()
        response = c.get(reverse("aimmo/play", kwargs={"id": 2}))
        self.assertEqual(response.status_code, 404)

    def _run_test_for_unauthorised_user(self, link, kwarg_name, status_code):
        self._make_game_private()
        c = self.login()
        response = c.get(reverse(link, kwargs={kwarg_name: 1}))
        self.assertEqual(response.status_code, status_code)

    def test_play_for_unauthorised_user(self):
        self._run_test_for_unauthorised_user("aimmo/play", "id", 404)

    def test_play_inactive_level(self):
        c = self.login()
        self.game.completed = True
        if self.game.is_active:
            self.skipTest("Completed game is active")
        self.game.static_data = '{"test": 1}'
        self.game.save()
        response = c.get(reverse("aimmo/play", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["active"])
        self.assertEqual(response.context["static_data"], '{"test": 1}')

    def test_games_api(self):
        self.game.main_user = self.user
        self.game.save()
        user2 = User.objects.create_user(username="2", password="password")
        user3 = User.objects.create_user(username="3", password="password")
        models.Avatar(owner=self.user, code=self.CODE, pk=1, game=self.game).save()
        models.Avatar(owner=user2, code="test2", pk=2, game=self.game).save()
        models.Avatar(owner=user3, code="test3", pk=3, game=self.game).save()
        c = Client()
        response = c.get(reverse("aimmo/game_details", kwargs={"id": 1}))
        self.assertJSONEqual(response.content, self.EXPECTED_GAMES)

    def test_games_api_for_non_existent_game(self):
        response = self._go_to_page("aimmo/game_details", "id", 5)
        self.assertEqual(response.status_code, 404)

    def _run_mark_complete_test(self, request_method, game_id, success_expected):
        c = Client()
        if request_method == "POST":
            response = c.post(reverse("aimmo/complete_game", kwargs={"id": game_id}))
        else:
            response = c.get(reverse("aimmo/complete_game", kwargs={"id": game_id}))
        self.assertEqual(response.status_code == 200, success_expected)
        self.assertEqual(models.Game.objects.get(id=1).completed, success_expected)

    def test_mark_complete(self):
        self._run_mark_complete_test("POST", 1, True)

    def test_mark_complete_for_non_existent_game(self):
        self._run_mark_complete_test("POST", 3, False)

    def test_mark_complete_requires_POST(self):
        self._run_mark_complete_test("GET", 1, False)

    def test_mark_complete_has_no_csrf_check(self):
        c = Client(enforce_csrf_checks=True)
        response = c.post(reverse("aimmo/complete_game", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Game.objects.get(id=1).completed)

    def test_mark_complete_with_data(self):
        c = Client()
        c.post(
            reverse("aimmo/complete_game", kwargs={"id": 1}),
            "static",
            content_type="application/json",
        )
        self.assertEqual(models.Game.objects.get(id=1).static_data, "static")

    def test_current_avatar_api_for_non_existent_game(self):
        response = self._go_to_page("aimmo/current_avatar_in_game", "game_id", 1)
        self.assertEqual(response.status_code, 404)

    def test_current_avatar_api_for_unauthorised_games(self):
        self._run_test_for_unauthorised_user(
            "aimmo/current_avatar_in_game", "game_id", 401
        )

    def test_current_avatar_api_for_two_users(self):
        # Set up the first avatar
        first_user = self.user
        models.Avatar(owner=first_user, code=self.CODE, game=self.game).save()
        client_one = self.login()

        # Set up the second avatar
        second_user = User.objects.create_user(
            "test2", "test2@example.com", "password2"
        )
        second_user.save()
        models.Avatar(owner=second_user, code=self.CODE, game=self.game).save()
        client_two = Client()
        client_two.login(username="test2", password="password2")

        self.game.public = True
        self.game.can_play = [first_user, second_user]
        self.game.save()

        first_response = client_one.get(
            reverse("aimmo/current_avatar_in_game", kwargs={"game_id": 1})
        )
        second_response = client_two.get(
            reverse("aimmo/current_avatar_in_game", kwargs={"game_id": 1})
        )

        # Status code starts with 2, success response can be different than 200.
        self.assertEqual(str(first_response.status_code)[0], "2")
        self.assertEqual(str(second_response.status_code)[0], "2")

        # JSON is returned as string so needs to be evaluated.
        first_id = ast.literal_eval(first_response.content)["current_avatar_id"]
        second_id = ast.literal_eval(second_response.content)["current_avatar_id"]

        self.assertEqual(first_id, 1)
        self.assertEqual(second_id, 2)

    def test_current_avatar_api_call_returns_404_for_logged_out_user(self):
        user = self.user
        models.Avatar(owner=user, code=self.CODE, game=self.game).save()
        client_one = Client()

        self.game.public = True
        self.game.can_play = [user]
        self.game.save()

        first_response = client_one.get(
            reverse("aimmo/current_avatar_in_game", kwargs={"game_id": 1})
        )

        self.assertEqual(first_response.status_code, 404)

    def test_id_of_current_avatar_same_as_games_url(self):
        """
        Ensures that the id's are consistent throughout the project. Check for ID's received
        by the current_avatar URL as well as the games URL api.
        """
        user = self.user
        models.Avatar(owner=user, code=self.CODE, game=self.game).save()
        client = self.login()

        self.game.public = True
        self.game.can_play = [user]
        self.game.save()

        current_avatar_api_response = client.get(
            reverse("aimmo/current_avatar_in_game", kwargs={"game_id": 1})
        )
        games_api_response = client.get(reverse("aimmo/game_details", kwargs={"id": 1}))

        current_avatar_id = ast.literal_eval(current_avatar_api_response.content)[
            "current_avatar_id"
        ]
        games_api_users = json.loads(games_api_response.content)["main"]["users"]

        self.assertEqual(current_avatar_id, 1)
        self.assertEqual(len(games_api_users), 1)
        self.assertEqual(games_api_users[0]["id"], 1)
