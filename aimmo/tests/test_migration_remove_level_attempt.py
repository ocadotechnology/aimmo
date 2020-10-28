from .base_test_migration import MigrationTestCase


class TestMigrationAddWorksheetModel(MigrationTestCase):
    start_migration = "0021_add_pdf_names_to_worksheet"
    dest_migration = "0022_remove_level_attempt"

    def test_worksheet_model_exists(self):
        model_names = [
            model._meta.db_table for model in self.django_application.get_models()
        ]
        assert "aimmo_levelattempt" not in model_names
