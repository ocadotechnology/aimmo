from django.contrib.auth.models import User
from django.test import TestCase

from aimmo.models import Game


class TestModels(TestCase):
    def test_game_owner_on_delete(self):
        """
        Given a game and a user, where the user is the owner of the game,
        When the user is deleted,
        Then the game's owner field is set to null.
        """
        user = User.objects.create_user("test", "test@example.com", "password")
        game = Game(id=1, name="Test Game", worksheet_id=1)
        game.owner = user
        game.save()

        user.delete()
        game = Game.objects.get(id=1)

        assert game.owner is None

    def test_game_main_user_on_delete(self):
        """
        Given a game and a user, where the user is the main user of the game,
        When the user is deleted,
        Then the game's main_user field is set to null.
        """
        user = User.objects.create_user("test", "test@example.com", "password")
        game = Game(id=1, name="Test Game", worksheet_id=1)
        game.main_user = user
        game.save()

        user.delete()
        game = Game.objects.get(id=1)

        assert game.main_user is None
