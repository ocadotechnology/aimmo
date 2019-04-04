from django.contrib.auth.models import User
from django.test import TestCase

from aimmo import models, forms, app_settings

app_settings.GAME_SERVER_URL_FUNCTION = lambda game_id: (
    "base %s" % game_id,
    "path %s" % game_id,
)
app_settings.GAME_SERVER_PORT_FUNCTION = lambda game_id: 0
app_settings.GAME_SERVER_SSL_FLAG = True


class TestForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user("test", "test@example.com", "password")
        cls.user1.save()
        cls.game = models.Game(id=1, name="test", public=False)
        cls.game.save()

    def test_create_game(self):
        form = forms.AddGameForm([self.game], {"name": "test2"})
        self.assertTrue(form.is_valid())
        new_game = form.save()
        self.assertEqual(new_game.name, "test2")

    def test_cannot_create_duplicate_game(self):
        form = forms.AddGameForm([self.game], {"name": "test"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors, {"__all__": [u"Sorry, a game with this name already exists."]}
        )
