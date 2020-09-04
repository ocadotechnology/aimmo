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
