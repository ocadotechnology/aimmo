from .base_test_migration import MigrationTestCase


class TestMigrationLinkClassToGame(MigrationTestCase):
    start_migration = "0015_game_worksheet"
    dest_migration = "0016_game_class"

    def test_game_has_worksheet_as_foreign_key(self):
        Game = self.django_application.get_model(self.app_name, "Game")

        self.assertEquals(
            Game._meta.get_field("game_class").get_internal_type(), "ForeignKey"
        )
