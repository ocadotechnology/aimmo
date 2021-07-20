import pytest


@pytest.mark.django_db
def test_game_has_worksheet_as_foreign_key(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0015_game_worksheet"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0016_game_class"))
    Game = new_state.apps.get_model("aimmo", "Game")

    assert Game._meta.get_field("game_class").get_internal_type() == "ForeignKey"
