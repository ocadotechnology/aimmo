from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase

from aimmo import models, app_settings

app_settings.GAME_SERVER_URL_FUNCTION = lambda game_id: (
    "base %s" % game_id,
    "path %s" % game_id,
)
app_settings.GAME_SERVER_PORT_FUNCTION = lambda game_id: 0
app_settings.GAME_SERVER_SSL_FLAG = True


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user("test", "test@example.com", "password")
        cls.user1.save()
        cls.user2 = User.objects.create_user("test2", "test2@example.com", "password")
        cls.user2.save()
        cls.game = models.Game(id=1, name="test", public=False)
        cls.game.save()

    def setUp(self):
        self.game.refresh_from_db()

    def _make_game_private_for_user(self, user):
        self.game.public = False
        self.game.can_play = [user]

    def _run_test_authorisation_to_play(self, user, can_play):
        self._make_game_private_for_user(self.user1)
        self.assertEqual(self.game.can_user_play(user), can_play)

    def test_public_games_can_be_accessed(self):
        self.game.public = True
        self.assertTrue(self.game.can_user_play(self.user1))
        self.assertTrue(self.game.can_user_play(self.user2))

    def test_anon_user_can_play_public_game(self):
        self.game.public = True
        self.assertTrue(self.game.can_user_play(AnonymousUser()))

    def test_authorised_user_can_play(self):
        self._run_test_authorisation_to_play(self.user1, True)

    def test_unauthorised_user_cannot_play(self):
        self._run_test_authorisation_to_play(self.user2, False)

    def test_game_active_by_default(self):
        self.assertTrue(self.game.is_active)

    def test_completed_game_inactive(self):
        self.game.completed = True
        self.game.save()
        self.assertFalse(self.game.is_active)
