import json
from common.models import Class, Teacher, UserProfile
from common.tests.utils.classes import create_class_directly
from common.tests.utils.student import (
    create_independent_student_directly,
    create_school_student_directly,
)
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from portal.forms.add_game import AddGameForm
from aimmo.game_creator import create_game
from rest_framework import status

from aimmo import app_settings, models
from aimmo.models import Game
from aimmo.serializers import GameSerializer
from aimmo.views import get_avatar_id
from aimmo.worksheets import WORKSHEETS, Worksheet
from unittest.mock import patch

app_settings.GAME_SERVER_URL_FUNCTION = lambda game_id: (
    "base %s" % game_id,
    "path %s" % game_id,
)
app_settings.GAME_SERVER_PORT_FUNCTION = lambda game_id: 0
app_settings.GAME_SERVER_SSL_FLAG = True


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

    @classmethod
    def setUpTestData(cls):
        cls.user: User = User.objects.create_user(
            "test", "test@example.com", "password"
        )
        cls.user.is_staff = True
        cls.user.save()
        user_profile: UserProfile = UserProfile(user=cls.user)
        user_profile.save()
        teacher: Teacher = Teacher.objects.create(user=user_profile, new_user=cls.user)
        teacher.save()
        cls.klass, _, _ = create_class_directly(cls.user.email)
        cls.klass.save()
        cls.klass2, _, _ = create_class_directly(cls.user.email)
        cls.klass2.save()
        cls.worksheet: Worksheet = WORKSHEETS.get(1)
        cls.worksheet2: Worksheet = WORKSHEETS.get(2)
        cls.game = models.Game(id=1, name="test", game_class=cls.klass, worksheet_id=1)
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

    def test_code_for_non_existent_game(self):
        c = self.login()
        response = c.post(reverse("kurono/code", kwargs={"id": 2}), {"code": self.CODE})
        self.assertEqual(response.status_code, 404)

    def test_code_for_non_authed_user(self):
        username, password, _ = create_independent_student_directly()
        c = self.login(username=username, password=password)
        response = c.post(reverse("kurono/code", kwargs={"id": 1}), {"code": self.CODE})
        self.assertEqual(response.status_code, 404)

    def test_worksheet_starter_code(self):
        c = self.login()
        response = c.get(reverse("kurono/code", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.worksheet.starter_code, json.loads(response.content)["code"]
        )

    def test_retrieve_code(self):
        models.Avatar(owner=self.user, code=self.CODE, game=self.game).save()
        c = self.login()
        response = c.get(reverse("kurono/code", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"code": self.CODE, "starterCode": self.game.worksheet.starter_code},
        )

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

        klass, _, _ = create_class_directly("test@example.com", "my class")

        form = AddGameForm(
            Class.objects.all(),
            data={"game_class": klass.id},
        )

        game2 = form.save()
        assert game2.game_class == klass

        data = {"game_ids": [game2.id]}
        response = client.post(reverse("game-delete-games"), data)

        assert response.status_code == 204
        assert models.Game.objects.all().count() == 2
        assert models.Game.objects.filter(is_archived=True).count() == 1
        assert models.Game.objects.filter(is_archived=False).count() == 1

        # then test adding game again for the same class
        form = AddGameForm(
            Class.objects.all(),
            data={"game_class": klass.id},
        )

        game3 = form.save()
        assert game3.game_class == klass

        # test only one active game at a time
        assert (
            models.Game.objects.filter(game_class=klass, is_archived=False).count() == 1
        )

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

        game2 = models.Game(id=2, name="test", game_class=self.klass2)
        game2.save()

        def expected_game_detail(class_id, worksheet_id):
            return {
                "era": "1",
                "name": "test",
                "status": "r",
                "settings": '{"GENERATOR": "Main", "OBSTACLE_RATIO": 0.1, "PICKUP_SPAWN_CHANCE": 0.1, "SCORE_DESPAWN_CHANCE": 0.05, "START_HEIGHT": 31, "START_WIDTH": 31, "TARGET_NUM_CELLS_PER_AVATAR": 16.0, "TARGET_NUM_PICKUPS_PER_AVATAR": 1.2, "TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR": 0.5}',
                "class_id": str(class_id),
                "worksheet_id": str(worksheet_id),
            }

        expected_game_list = {
            "1": expected_game_detail(self.klass.id, self.worksheet.id),
            "2": expected_game_detail(self.klass2.id, 1),
        }

        c = Client()
        response = c.get(reverse("game-list"))

        self.assertJSONEqual(response.content, expected_game_list)

    def test_view_one_game(self):
        client = self.login()
        response = client.get(reverse("game-detail", kwargs={"pk": self.game.id}))
        self.assertEqual(response.status_code, 200)

    @patch("aimmo.game_creator.GameManager")
    def test_adding_a_game_creates_an_avatar(self, mock_game_manager):
        client = self.login()
        game: Game = create_game(
            self.user,
            AddGameForm(
                Class.objects.all(),
                data={
                    "game_class": self.klass2.id,
                },
            ),
        )

        # GameManager is called when a game is created.
        assert mock_game_manager.called

        game = models.Game.objects.get(pk=2)
        avatar = game.avatar_set.get(owner=client.session["_auth_user_id"])
        assert avatar is not None

    @patch("aimmo.serializers.GameManager")
    def test_update_game_worksheet_updates_avatar_codes(self, mock_game_manager):
        # Set up the first avatar
        first_user = self.user
        models.Avatar(owner=first_user, code=self.CODE, game=self.game).save()
        client1 = self.login()

        # Set up the second avatar
        _, _, second_user = create_school_student_directly(self.klass.access_code)
        models.Avatar(owner=second_user.new_user, code=self.CODE, game=self.game).save()

        client2 = Client()
        client2.login(username="test2", password="password2")

        data = json.dumps({"worksheet_id": self.worksheet2.id})

        response = client1.put(
            reverse("game-detail", kwargs={"pk": self.game.id}),
            data,
            content_type="application/json",
        )

        # GameManager is called when a game is edited.
        assert mock_game_manager.called
        assert response.status_code == 200

        game = models.Game.objects.get(id=1)
        avatar1 = models.Avatar.objects.get(id=1)
        avatar2 = models.Avatar.objects.get(id=2)

        assert game.worksheet == self.worksheet2

        assert avatar1.code == self.worksheet2.starter_code
        assert avatar2.code == self.worksheet2.starter_code

    def test_delete_games(self):
        # Create a new teacher with a game to make sure it's not affected
        new_user: User = User.objects.create_user(
            "test2", "test2@example.com", "password"
        )
        new_user.is_staff = True
        new_user.save()
        new_user_profile: UserProfile = UserProfile(user=new_user)
        new_user_profile.save()
        new_teacher: Teacher = Teacher.objects.create(
            user=new_user_profile, new_user=new_user
        )
        new_teacher.save()
        new_klass, _, _ = create_class_directly(new_user.email)
        new_user.save()
        new_game = models.Game(name="test2", game_class=new_klass, worksheet_id=1)
        new_game.save()

        # Create a game for the second class
        game2 = models.Game(name="test", game_class=self.klass2, worksheet_id=1)
        game2.save()

        data = {"game_ids": [self.game.id, game2.id, new_game.id]}

        # Try to login as a student and delete games - they shouldn't have access
        _, student_password, student = create_school_student_directly(
            self.klass.access_code
        )
        client = self.login(
            username=student.new_user.username, password=student_password
        )
        response = client.post(reverse("game-delete-games"), data)
        assert response.status_code == 403
        assert Game.objects.filter(is_archived=False).count() == 3
        assert Game.objects.filter(is_archived=True).count() == 0

        # Login as initial teacher and delete games - only his games should be deleted
        client = self.login()
        response = client.post(reverse("game-delete-games"), data)
        assert response.status_code == 204
        assert Game.objects.filter(is_archived=False).count() == 1
        assert Game.objects.filter(is_archived=True).count() == 2
        assert Game.objects.get(pk=new_game.id)

    def test_list_running_games(self):
        self.game.main_user = self.user
        self.game.save()

        klass3, _, _ = create_class_directly(self.user.email)
        klass3.save()
        klass4, _, _ = create_class_directly(self.user.email)
        klass4.save()

        game2 = Game(id=2, name="test", game_class=self.klass2, status=Game.STOPPED)
        game2.save()
        game3 = Game(id=3, name="test", game_class=klass3, status=Game.RUNNING)
        game3.save()
        game4 = Game(id=4, name="test", game_class=klass4, status=Game.STOPPED)
        game3.save()

        def expected_game_detail(class_id, worksheet_id):
            return {
                "era": "1",
                "name": "test",
                "status": "r",
                "settings": '{"GENERATOR": "Main", "OBSTACLE_RATIO": 0.1, "PICKUP_SPAWN_CHANCE": 0.1, "SCORE_DESPAWN_CHANCE": 0.05, "START_HEIGHT": 31, "START_WIDTH": 31, "TARGET_NUM_CELLS_PER_AVATAR": 16.0, "TARGET_NUM_PICKUPS_PER_AVATAR": 1.2, "TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR": 0.5}',
                "class_id": str(class_id),
                "worksheet_id": str(worksheet_id),
            }

        expected_game_list = {
            "1": expected_game_detail(self.klass.id, self.worksheet.id),
            "3": expected_game_detail(klass3.id, 1),
        }

        c = Client()
        response = c.get(reverse("game-running"))

        self.assertJSONEqual(response.content, expected_game_list)
