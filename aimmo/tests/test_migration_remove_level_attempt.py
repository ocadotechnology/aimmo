from .base_test_migration import MigrationTestCase


class TestMigrationRemoveLevelAttemptModel(MigrationTestCase):
    start_migration = "0022_allow_games_to_have_no_name"
    dest_migration = "0023_remove_level_attempt"

    def test_level_attempt_model_removed(self):
        model_names = [
            model._meta.db_table for model in self.django_application.get_models()
        ]
        assert "aimmo_levelattempt" not in model_names
