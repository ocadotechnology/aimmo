from typing import Tuple, List
from unittest.mock import patch

import pytest
from _pytest.monkeypatch import MonkeyPatch
from common.models import Class
from common.tests.utils.classes import create_class_directly
from common.tests.utils.organisation import create_organisation_directly
from common.tests.utils.student import create_school_student_directly
from common.tests.utils.teacher import signup_teacher_directly
from django.test import Client, TestCase
from django.urls import reverse

from aimmo.exceptions import GameLimitExceeded
from aimmo.models import Game, MAX_GAMES_LIMIT

MOCKED_MAX_GAMES_LIMIT = 2


class TestGameLimitExceededMiddleware(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.teacher_email, self.teacher_password = self._setup_teacher()
        self.classes = self._setup_classes(self.teacher_email)

        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr("aimmo.models.MAX_GAMES_LIMIT", MOCKED_MAX_GAMES_LIMIT)

    def tearDown(self) -> None:
        self.monkeypatch.setattr("aimmo.models.MAX_GAMES_LIMIT", MAX_GAMES_LIMIT)

    def _setup_teacher(self) -> Tuple[str, str]:
        teacher_email, teacher_password = signup_teacher_directly()
        create_organisation_directly(teacher_email)
        _, _, access_code = create_class_directly(teacher_email)
        create_school_student_directly(access_code)

        return teacher_email, teacher_password

    def _setup_classes(self, teacher_email: str) -> List[Class]:
        class1, _, access_code1 = create_class_directly(teacher_email)
        class2, _, access_code2 = create_class_directly(teacher_email)
        class3, _, access_code3 = create_class_directly(teacher_email)

        create_school_student_directly(access_code1)
        create_school_student_directly(access_code2)
        create_school_student_directly(access_code3)

        return [class1, class2, class3]

    def _student_login(self, access_code, student_name, student_password):
        return self.client.post(
            reverse("student_login", kwargs={"access_code": access_code}),
            {"username": student_name, "password": student_password},
            follow=True,
        )

    def test_cannot_create_game_when_max_limit_reached(self):
        """
        Given two already running games,
        When a teacher tries to create a third one,
        The teacher should be redirected to the Kurono dashboard with a message, and the game shouldn't be created.
        """
        game1 = Game(id=1, name="game1", game_class=self.classes[0], worksheet_id=1)
        game1.save()

        game2 = Game(id=2, name="game2", game_class=self.classes[1], worksheet_id=1)
        game2.save()

        self.client.login(username=self.teacher_email, password=self.teacher_password)

        response = self.client.post(reverse("teacher_aimmo_dashboard"), {"game_class": self.classes[2].id})

        assert response.status_code == 302
        assert response.url == "/teach/kurono/dashboard/"
        messages = list(response.wsgi_request._messages)
        assert len(messages) > 0
        assert (
            str(messages[0])
            == "The game is at full capacity. Please wait until someone returns from a mission and frees up a vessel. Please try again later."
        )
        assert Game.objects.all().count() == 2

    @patch("aimmo.views.GameManager")
    def test_cannot_start_stopped_game_when_max_limit_reached(self, mock_game_manager):
        """
        Given two running games and one stopped game,
        When a teacher or a student tries to play the stopped game,
        The user should be redirected to their respective dashboard with a message, and the game should remain stopped.
        """
        game1 = Game(id=1, name="game1", game_class=self.classes[0], worksheet_id=1)
        game1.save()

        game2 = Game(id=2, name="game2", game_class=self.classes[1], worksheet_id=1)
        game2.save()

        game3 = Game(id=3, name="game3", game_class=self.classes[2], worksheet_id=1, status=Game.STOPPED)
        game3.save()

        self.client.login(username=self.teacher_email, password=self.teacher_password)

        response = self.client.get(reverse("kurono/play", kwargs={"id": game3.id}))

        assert response.status_code == 302
        assert response.url == "/teach/kurono/dashboard/"
        messages = list(response.wsgi_request._messages)
        assert len(messages) > 0
        assert (
            str(messages[0])
            == "The game is at full capacity. Please wait until someone returns from a mission and frees up a vessel. Please try again later."
        )
        assert Game.objects.filter(status=Game.RUNNING).count() == 2

        game3 = Game.objects.get(id=3)

        assert game3.status == Game.STOPPED

        self.client.logout()

        class3 = self.classes[2]
        student = class3.students.all()[0]

        self._student_login(class3.access_code, student.new_user.first_name, "Password2")

        response = self.client.get(reverse("kurono/play", kwargs={"id": game3.id}))

        assert response.status_code == 302
        assert response.url == "/play/kurono/dashboard/"
        messages = list(response.wsgi_request._messages)
        assert len(messages) > 0
        assert (
            str(messages[0])
            == "Oh no! It seems there are too many time travellers active already. You'll need to wait until someone returns from a mission and frees up a ship. Please try again later."
        )
        assert Game.objects.filter(status=Game.RUNNING).count() == 2

        game3 = Game.objects.get(id=3)

        assert game3.status == Game.STOPPED

    def test_can_update_games_when_max_limit_reached(self):
        """
        Given two running games,
        When a change is being made to a game,
        That change can still be executed and doesn't raise a GameLimitExceeded exception.
        """
        game1 = Game(id=1, name="game1", game_class=self.classes[0], worksheet_id=1)
        game1.save()

        game2 = Game(id=2, name="game2", game_class=self.classes[1], worksheet_id=1)
        game2.save()

        game1.game_class = self.classes[2]
        game1.save()

        assert game1.game_class == self.classes[2]

    def test_cannot_update_games_to_exceed_max_limit(self):
        """
        Given one running game, and two stopped games,
        When update() would cause the amount of running games to exceed the limit,
        A GameLimitExceeded exception should be raised and the stopped games should remain stopped.
        """
        game1 = Game(id=1, name="game1", game_class=self.classes[0], worksheet_id=1)
        game1.save()

        game2 = Game(id=2, name="game2", game_class=self.classes[1], worksheet_id=1, status=Game.STOPPED)
        game2.save()

        game3 = Game(id=3, name="game3", game_class=self.classes[2], worksheet_id=1, status=Game.STOPPED)
        game3.save()

        stopped_games = Game.objects.filter(status=Game.STOPPED)

        with pytest.raises(GameLimitExceeded):
            stopped_games.update(status=Game.RUNNING)

        assert Game.objects.filter(status=Game.RUNNING).count() == 1
        assert Game.objects.filter(status=Game.STOPPED).count() == 2

        # Check update() still works if not exceeding the limit
        game1.delete()

        stopped_games.update(status=Game.RUNNING)

        assert Game.objects.filter(status=Game.RUNNING).count() == 2
        assert Game.objects.all().count() == 2
