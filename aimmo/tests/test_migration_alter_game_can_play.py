from __future__ import absolute_import
from .base_test_migration import MigrationTestCase


class TestMigrationAlterGameToken(MigrationTestCase):
    start_migration = "0012_auto_20200302_1310"
    dest_migration = "0013_alter_game_can_play"

    def test_game_can_play_description_altered(self):
        model = self.django_application.get_model(self.app_name, "Game")

        self.assertEquals(
            model._meta.get_field("can_play").help_text,
            "List of auth_user IDs of users who are allowed to play and have access to the game.",
        )
