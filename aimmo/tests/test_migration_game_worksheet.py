from .base_test_migration import MigrationTestCase


class TestMigrationLinkWorksheetWithGame(MigrationTestCase):
    start_migration = "0014_add_worksheet_model"
    dest_migration = "0015_game_worksheet"

    def test_game_has_worksheet_as_foreign_key(self):
        Worksheet = self.django_application.get_model(self.app_name, "Worksheet")
        Game = self.django_application.get_model(self.app_name, "Game")

        test_worksheet = Worksheet.objects.create(
            id=1, name="Test", starter_code="code"
        )
        test_worksheet.save()
        test_game = Game.objects.create(id=1, name="test", public=True)
        test_game.worksheet = test_worksheet
        test_game.save()

        self.assertEqual(test_game.worksheet.id, test_worksheet.id)
