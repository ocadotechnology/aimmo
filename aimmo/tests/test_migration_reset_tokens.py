from importlib import import_module

from django.apps import apps
from django.db import connection
from django.test import TestCase

from aimmo.models import Game

# Our filename starts with a number, so we use import_module
data_migration = import_module("aimmo.migrations.0011_reset_game_tokens")


class ResetGameTokensTests(TestCase):
    def __init__(self, *args, **kwargs):
        super(ResetGameTokensTests, self).__init__(*args, **kwargs)

        self.token = "I AM A TOKEN!"

    def test_reset_token(self):
        game = Game.objects.create(id=1, name="test", public=True)
        game.auth_token = self.token
        game.save()

        data_migration.reset_tokens(apps, connection.schema_editor())

        game = Game.objects.get(id=1)
        self.assertEqual(game.auth_token, "")
