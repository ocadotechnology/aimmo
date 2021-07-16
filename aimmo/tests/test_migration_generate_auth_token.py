from django.db.migrations.state import StateApps
from django.contrib.auth.models import User

from .base_test_migration import MigrationTestCase


class TestMigrationAddsAuthTokens(MigrationTestCase):
    start_migration = "0024_unique_class_per_game"
    dest_migration = "0025_generate_auth_token"

    def setUpDataBeforeMigration(self, django_application: StateApps):
        Game = django_application.get_model(self.app_name, "Game")

        # Teacher = django_application.get_model("common", "Teacher")
        # UserProfile = django_application.get_model("common", "UserProfile")
        # Class = django_application.get_model("common", "Class")
        # user = User.objects.create_user(
        #     username="a",
        #     email="email",
        #     password="password",
        #     first_name="first_name",
        #     last_name="last_name",
        # )
        # user_profile = UserProfile.objects.create(user=user)
        # teacher = Teacher.objects.create(
        #     user=user_profile, new_user=user, title="title"
        # )
        # teacher.save()
        # klass = Class.objects.create(teacher=teacher)
        # klass.save()

        # game = Game.objects.create(game_class=klass)
        # WIP: Errors with "FOREIGN KEY constraint failed" when all tests are run
        game = Game.objects.create()
        game.save()
        self.game_id = game.id

    def test_new_game_has_auth_token(self):
        Game = self.django_application.get_model(self.app_name, "Game")
        game = Game.objects.get(id=self.game_id)
        assert game.auth_token != "" and len(game.auth_token) > 0
