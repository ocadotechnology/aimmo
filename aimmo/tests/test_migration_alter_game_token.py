from base_test_migration import MigrationTestCase


class TestMigrationAlterGameToken(MigrationTestCase):

    start_migration = "0009_add_game_status"
    dest_migration = "0010_alter_game_token"

    def test_game_token_field_altered(self):
        model = self.django_application.get_model(self.app_name, "Game")
        game = model.objects.create(id=1, name="test", public=True)

        self.assertEquals(game.auth_token, "")
