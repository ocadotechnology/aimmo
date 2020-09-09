from django.db.migrations.state import StateApps

from .base_test_migration import MigrationTestCase


class TestMigrationAddFirstTwoWorksheets(MigrationTestCase):
    start_migration = "0016_game_class"
    dest_migration = "0017_add_worksheet_1_and_2"

    def test_first_two_worksheets_added(self):
        Worksheet = self.django_application.get_model(self.app_name, "Worksheet")
        all_worksheets = Worksheet.objects.all()

        assert all_worksheets.count() == 2


class TestMigrationAddFirstTwoWorksheetsBackward(MigrationTestCase):
    start_migration = "0017_add_worksheet_1_and_2"
    dest_migration = "0016_game_class"

    def test_no_worksheets_after_rollback(self):
        Worksheet = self.django_application.get_model(self.app_name, "Worksheet")
        all_worksheets = Worksheet.objects.all()

        assert all_worksheets.count() == 0


class TestMigrationWorksheet2AsDefault(MigrationTestCase):
    start_migration = "0017_add_worksheet_1_and_2"
    dest_migration = "0018_set_worksheet_2_as_default_for_games"

    def setUpDataBeforeMigration(self, django_application: StateApps):
        Game = django_application.get_model(self.app_name, "Game")
        Worksheet = django_application.get_model(self.app_name, "Worksheet")
        worksheet1 = Worksheet.objects.get(name="Present Day I: The Museum")
        game_with_worksheet = Game.objects.create(
            name="game with worksheet before migration", worksheet=worksheet1
        )
        game_with_worksheet.save()
        game_without_worksheet = Game.objects.create(
            name="game without worksheet before migration"
        )
        game_without_worksheet.save()
        assert game_without_worksheet.worksheet is None

    def test_worksheet_2_is_default_for_games_without_one(self):
        Game = self.django_application.get_model(self.app_name, "Game")
        Worksheet = self.django_application.get_model(self.app_name, "Worksheet")
        worksheet2 = Worksheet.objects.get(name="Present Day II")
        game_with_worksheet = Game.objects.get(
            name="game with worksheet before migration"
        )
        game_without_worksheet = Game.objects.get(
            name="game without worksheet before migration"
        )
        assert game_with_worksheet.worksheet is not None
        assert game_without_worksheet.worksheet is not None
        assert game_with_worksheet.worksheet.name == "Present Day I: The Museum"
        assert game_without_worksheet.worksheet.name == "Present Day II"
