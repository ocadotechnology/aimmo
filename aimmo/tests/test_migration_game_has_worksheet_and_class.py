from aimmo.tests.base_test_migration import MigrationTestCase


class TestMigrationGameHasWorksheetAndClass(MigrationTestCase):
    start_migration = "0018_set_worksheet_2_as_default_for_games"
    dest_migration = "0019_game_has_worksheet_and_class"

    def test_game_class_verbose_name(self):
        Game = self.django_application.get_model(self.app_name, "Game")
        assert Game._meta.get_field("game_class").verbose_name == "Class"

    def test_worksheet_is_required_and_not_empty(self):
        Game = self.django_application.get_model(self.app_name, "Game")
        worksheet_field = Game._meta.get_field("worksheet")
        assert not worksheet_field.null
        assert not worksheet_field.blank
