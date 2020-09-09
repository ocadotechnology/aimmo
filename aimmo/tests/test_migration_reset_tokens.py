from django.db.migrations.state import StateApps

from aimmo.tests.base_test_migration import MigrationTestCase


class TestMigrationResetGameTokens(MigrationTestCase):
    start_migration = "0010_alter_game_token"
    dest_migration = "0011_reset_game_tokens"

    def setUpDataBeforeMigration(self, django_application: StateApps):
        Game = django_application.get_model(self.app_name, "Game")
        game = Game.objects.create(id=1, name="test", public=True)
        game.auth_token = "I'm a token"
        game.save()

    def test_reset_token(self):
        Game = self.django_application.get_model(self.app_name, "Game")
        game = Game.objects.get(id=1)
        assert game.auth_token == ""
