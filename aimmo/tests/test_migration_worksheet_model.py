from __future__ import absolute_import

from .base_test_migration import MigrationTestCase


class TestMigrationAlterGameToken(MigrationTestCase):
    start_migration = "0013_alter_game_can_play"
    dest_migration = "0014_add_worksheet_model"

    def test_worksheet_model_exists(self):
        model_names = [
            model._meta.db_table for model in self.django_application.get_models()
        ]
        assert "aimmo_worksheet" in model_names

    def test_worksheet_has_correct_fields(self):
        model = self.django_application.get_model(self.app_name, "Worksheet")

        self.assertEquals(
            model._meta.get_field("name").get_internal_type(), "CharField"
        )
        self.assertEquals(
            model._meta.get_field("era").get_internal_type(),
            "PositiveSmallIntegerField",
        )
        self.assertEquals(
            model._meta.get_field("starter_code").get_internal_type(), "TextField"
        )
