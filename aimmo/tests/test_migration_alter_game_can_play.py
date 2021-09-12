import pytest


@pytest.mark.django_db
def test_game_can_play_description_altered(migrator):
    migrator.apply_initial_migration(("aimmo", "0012_auto_20200302_1310"))
    new_state = migrator.apply_tested_migration(("aimmo", "0013_alter_game_can_play"))
    model = new_state.apps.get_model("aimmo", "Game")

    assert (
        model._meta.get_field("can_play").help_text
        == "List of auth_user IDs of users who are allowed to play and have access to the game."
    )
