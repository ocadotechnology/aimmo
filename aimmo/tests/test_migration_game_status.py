from base_test_migration import MigrationTestCase


class TestMigrationPreviewUsers(MigrationTestCase):

    start_migration = "0008_default_public_field"
    dest_migration = "0009_add_game_status"

    def test_game_status_field_added(self):
        model = self.django_application.get_model(self.app_name, "Game")

        self.assertEquals(
            model._meta.get_field("status").get_internal_type(), "CharField"
        )
