import pytest


@pytest.mark.django_db
def test_game_token_field_altered(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0009_add_game_status"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0010_alter_game_token"))
    model = new_state.apps.get_model("aimmo", "Game")
    game = model.objects.create(id=1, name="test", public=True)

    assert game.auth_token == ""
