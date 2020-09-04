import json

import pytest
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from rest_framework import status

from aimmo import app_settings, models
from aimmo.forms import AddGameForm
from aimmo.game_creator import create_game
from aimmo.models import Game
from aimmo.serializers import GameSerializer
from aimmo.views import get_avatar_id
from common.models import Class, Student, Teacher, UserProfile
from common.tests.utils.classes import create_class_directly
from common.tests.utils.student import (
    create_independent_student_directly,
    create_school_student_directly,
)

app_settings.GAME_SERVER_URL_FUNCTION = lambda game_id: (
    "base %s" % game_id,
    "path %s" % game_id,
)
app_settings.GAME_SERVER_PORT_FUNCTION = lambda game_id: 0
app_settings.GAME_SERVER_SSL_FLAG = True
DEFAULT_CODE = """def next_turn(world_state, avatar_state):
    return MoveAction(direction.NORTH)
"""


class TestViews(TestCase):
    CODE = "class Avatar: pass"

    EXPECTED_GAMES = {
        "main_avatar": 1,
        "users": [
            {"id": 1, "code": CODE},
            {"id": 2, "code": "test2"},
            {"id": 3, "code": "test3"},
        ],
    }

    EXPECTED_GAME_DETAIL = {
        "era": "1",
        "name": "test",
        "status": "r",
        "settings": '{"GENERATOR": "Main", "OBSTACLE_RATIO": 0.1, "PICKUP_SPAWN_CHANCE": 0.1, "SCORE_DESPAWN_CHANCE": 0.05, "START_HEIGHT": 31, "START_WIDTH": 31, "TARGET_NUM_CELLS_PER_AVATAR": 16.0, "TARGET_NUM_PICKUPS_PER_AVATAR": 1.2, "TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR": 0.5}',
        "worksheet_id": "2",
    }

    EXPECTED_GAME_LIST = {"1": EXPECTED_GAME_DETAIL, "2": EXPECTED_GAME_DETAIL}

    @classmethod
    def setUpTestData(cls):
        cls.user: User = User.objects.create_user(
            "test", "test@example.com", "password"
        )
        cls.user.is_staff = True
        cls.user.save()
        user_profile: UserProfile = UserProfile(user=cls.user)
        user_profile.save()
        teacher: Teacher = Teacher.objects.create(
            user=user_profile, new_user=cls.user, title="Mx"
        )
        teacher.save()
        cls.klass, _, _ = create_class_directly(cls.user.email)
        cls.klass.save()
        cls.game = models.Game(
            id=1,
            name="test",
            game_class=cls.klass,
        )
        cls.game.save()

    def setUp(self):
        self.game.refresh_from_db()

    def login(self, username: str = "test", password: str = "password"):
        c = Client()
        c.login(username=username, password=password)
        return c

    def _go_to_page(self, link, kwarg_name, game_id):
        c = Client()
        response = c.get(reverse(link, kwargs={kwarg_name: game_id}))
        return response

    def test_add_new_code(self):
        c = self.login()
        response = c.post(reverse("kurono/code", kwargs={"id": 1}), {"code": self.CODE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            models.Avatar.objects.get(owner__username="test").code, self.CODE
        )

    def test_update_code(self):
        c = self.login()
        models.Avatar(owner=self.user, code="test", game=self.game).save()
        response = c.post(reverse("kurono/code", kwargs={"id": 1}), {"code": self.CODE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            models.Avatar.objects.get(owner__username="test").code, self.CODE
        )

    def test_code_for_non_existant_game(self):
        c = self.login()
        response = c.post(reverse("kurono/code", kwargs={"id": 2}), {"code": self.CODE})
        self.assertEqual(response.status_code, 404)

    def test_code_for_non_authed_user(self):
        username, password, _ = create_independent_student_directly()
        c = self.login(username=username, password=password)
        response = c.post(reverse("kurono/code", kwargs={"id": 1}), {"code": self.CODE})
        self.assertEqual(response.status_code, 404)

    def test_default_code(self):
        c = self.login()
        response = c.get(reverse("kurono/code", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DEFAULT_CODE, json.loads(response.content)["code"])

    def test_retrieve_code(self):
        models.Avatar(owner=self.user, code=self.CODE, game=self.game).save()
        c = self.login()
        response = c.get(reverse("kurono/code", kwargs={"id": 1}))
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
        response = c.get(reverse("kurono/play", kwargs={"id": 1}))
        assert response.status_code == 200
        assert response.context["current_user_player_key"] == self.user.pk
        assert response.context["game_url_base"] == "base 1"
        assert response.context["game_url_path"] == "path 1"

    def test_play_for_non_existent_game(self):
        c = self.login()
        response = c.get(reverse("kurono/play", kwargs={"id": 2}))
        self.assertEqual(response.status_code, 404)

    def test_play_for_unauthorised_user(self):
        username, password, _ = create_independent_student_directly()
        c = self.login(username=username, password=password)
        response = c.get(reverse("kurono/play", kwargs={"id": 1}))
        assert response.status_code == 404

    def test_play_inactive_level(self):
        c = self.login()
        self.game.completed = True
        if self.game.is_active:
            self.skipTest("Completed game is active")
        self.game.static_data = '{"test": 1}'
        self.game.save()
        response = c.get(reverse("kurono/play", kwargs={"id": 1}))
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
        response = c.get(reverse("kurono/game_user_details", kwargs={"id": 1}))
        self.assertJSONEqual(response.content, self.EXPECTED_GAMES)

    def test_games_api_for_non_existent_game(self):
        response = self._go_to_page("kurono/game_user_details", "id", 5)
        self.assertEqual(response.status_code, 404)

    def _run_mark_complete_test(self, request_method, game_id, success_expected):
        c = Client()
        if request_method == "POST":
            response = c.post(reverse("kurono/complete_game", kwargs={"id": game_id}))
        else:
            response = c.get(reverse("kurono/complete_game", kwargs={"id": game_id}))
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
        response = c.post(reverse("kurono/complete_game", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Game.objects.get(id=1).completed)

    def test_mark_complete_with_data(self):
        c = Client()
        c.post(
            reverse("kurono/complete_game", kwargs={"id": 1}),
            "static",
            content_type="application/json",
        )
        self.assertEqual(models.Game.objects.get(id=1).static_data, "static")

    def test_stop_game(self):
        game = models.Game.objects.get(id=1)
        game.auth_token = "tokenso lorenzo"
        game.save()
        c = Client()

        response = c.patch(
            reverse("game-detail", kwargs={"pk": 1}),
            json.dumps({"status": models.Game.STOPPED}),
            content_type="application/json",
            HTTP_GAME_TOKEN=game.auth_token,
        )
        game = models.Game.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(game.status, models.Game.STOPPED)

    def test_stop_game_no_token(self):
        game = models.Game.objects.get(id=1)
        game.auth_token = "tokenso lorenzo"
        game.save()
        c = Client()

        response = c.patch(
            reverse("game-detail", kwargs={"pk": 1}),
            json.dumps({"status": models.Game.STOPPED}),
            content_type="application/json",
        )
        game = models.Game.objects.get(id=1)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(game.status, models.Game.RUNNING)

    def test_get_avatar_id_for_non_existent_game(self):
        _, response = get_avatar_id(self.user, 1)
        assert response.status_code == 404

    def test_get_avatar_id_for_unauthorised_games(self):
        _, _, independent_student = create_independent_student_directly()
        _, response = get_avatar_id(independent_student.new_user, 1)
        assert response.status_code == 401

    def test_get_avatar_id_for_two_users(self):
        # Set up the first avatar
        first_user = self.user
        models.Avatar(owner=first_user, code=self.CODE, game=self.game).save()
        client_one = self.login()

        # Set up the second avatar
        _, _, second_user = create_school_student_directly(self.klass.access_code)
        models.Avatar(owner=second_user.new_user, code=self.CODE, game=self.game).save()
        client_two = Client()
        client_two.login(username="test2", password="password2")

        first_avatar_id, first_response = get_avatar_id(first_user, 1)
        second_avatar_id, second_response = get_avatar_id(second_user.new_user, 1)

        # Status code starts with 2, success response can be different than 200.
        assert str(first_response.status_code)[0] == "2"
        assert str(second_response.status_code)[0] == "2"

        assert first_avatar_id == 1
        assert second_avatar_id == 2

    def test_connection_parameters_api_call_returns_404_for_logged_out_user(self):
        user = self.user
        models.Avatar(owner=user, code=self.CODE, game=self.game).save()
        client_one = Client()

        self.game.public = True
        self.game.can_play.set([user])
        self.game.save()

        first_response = client_one.get(
            reverse("kurono/connection_parameters", kwargs={"game_id": 1})
        )

        assert first_response.status_code == 403

    def test_id_of_connection_parameters_same_as_games_url(self):
        """
        Ensures that the id's are consistent throughout the project. Check for ID's received
        by the current_avatar URL as well as the games URL api.
        """
        user = self.user
        models.Avatar(owner=user, code=self.CODE, game=self.game).save()
        client = self.login()

        connection_parameters_response = client.get(
            reverse("kurono/connection_parameters", kwargs={"game_id": 1})
        ).json()
        games_api_response = client.get(
            reverse("kurono/game_user_details", kwargs={"id": 1})
        )

        current_avatar_id = connection_parameters_response["avatar_id"]
        games_api_users = json.loads(games_api_response.content)["users"]

        self.assertEqual(current_avatar_id, 1)
        self.assertEqual(len(games_api_users), 1)
        self.assertEqual(games_api_users[0]["id"], 1)

    def test_token_view_get_token_multiple_requests(self):
        """
        Ensures we can make a get request for the token, and
        that a request with a valid token is also accepted.
        """
        token = models.Game.objects.get(id=1).auth_token
        client = Client()
        response = client.get(reverse("kurono/game_token", kwargs={"id": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(token, response.json()["token"])

        # Token starts as empty, as long as it is empty, we can make more GET requests
        response = client.get(reverse("kurono/game_token", kwargs={"id": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(token, response.json()["token"])

    def test_get_token_after_token_set(self):
        token = models.Game.objects.get(id=1).auth_token
        client = Client()
        response = client.get(reverse("kurono/game_token", kwargs={"id": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(token, response.json()["token"])

        new_token = "aaaaaaaaaaa"
        response = client.patch(
            reverse("kurono/game_token", kwargs={"id": 1}),
            json.dumps({"token": new_token}),
            content_type="application/json",
        )

        # Token starts as empty, as long as it is empty, we can make more GET requests
        response = client.get(
            reverse("kurono/game_token", kwargs={"id": 1}), HTTP_GAME_TOKEN=new_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_token_with_no_token(self):
        """
        Check for 401 when attempting to change game token.
        """
        client = Client()
        token = models.Game.objects.get(id=1).auth_token
        response = client.patch(reverse("kurono/game_token", kwargs={"id": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_token_with_incorrect_token(self):
        """
        Check for 403 when attempting to change game token (incorrect token provided).
        """
        client = Client()
        token = models.Game.objects.get(id=1).auth_token
        response = client.patch(
            reverse("kurono/game_token", kwargs={"id": 1}),
            {},
            content_type="application/json",
            HTTP_GAME_TOKEN="INCORRECT TOKEN",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_token_with_correct_token(self):
        """
        Check for 200 and successful token change when updating the token (correct token provided).
        """
        client = Client()
        token = models.Game.objects.get(id=1).auth_token
        new_token = token[::-1]
        response = client.patch(
            reverse("kurono/game_token", kwargs={"id": 1}),
            json.dumps({"token": new_token}),
            content_type="application/json",
            HTTP_GAME_TOKEN=token,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Game.objects.get(id=1).auth_token, new_token)

    def test_delete_game(self):
        """
        Check for 204 when deleting a game
        """
        client = self.login()

        game2 = models.Game(id=2, name="test", public=True)
        game2.save()

        response = client.delete(reverse("game-detail", kwargs={"pk": self.game.id}))
        self.assertEquals(response.status_code, 204)
        self.assertEquals(len(models.Game.objects.all()), 1)

    def test_delete_non_existent_game(self):
        c = self.login()
        response = c.delete(reverse("game-detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 404)

    def test_delete_for_unauthorized_user(self):
        """
        Check for 403 when attempting to delete a game without being authorized
        """
        username, password, _ = create_independent_student_directly()
        c = self.login(username=username, password=password)
        response = c.delete(reverse("game-detail", kwargs={"pk": self.game.id}))
        self.assertEqual(response.status_code, 403)

    def test_game_serializer_settings(self):
        """
        Check that the serializer gets the correct settings data from the game
        """
        client = self.login()

        serializer = GameSerializer(self.game)

        self.assertEquals(
            json.dumps(self.game.settings_as_dict(), sort_keys=True),
            serializer.data["settings"],
        )

    def test_list_all_games(self):
        self.game.main_user = self.user
        self.game.save()

        game2 = models.Game(id=2, name="test", public=True)
        game2.save()

        c = Client()
        response = c.get(reverse("game-list"))

        self.assertJSONEqual(response.content, self.EXPECTED_GAME_LIST)

    def test_view_one_game(self):
        client = self.login()
        response = client.get(reverse("game-detail", kwargs={"pk": self.game.id}))
        self.assertEqual(response.status_code, 200)

    def test_adding_a_game_creates_an_avatar(self):
        client = self.login()
        game: Game = create_game(
            self.user,
            AddGameForm(
                Class.objects.all(),
                data={"name": "new game", "game_class": self.klass.id},
            ),
        )
        game = models.Game.objects.get(pk=2)
        avatar = game.avatar_set.get(owner=client.session["_auth_user_id"])
        assert avatar is not None
