import pytest


@pytest.mark.django_db
def test_game_class_verbose_name(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0018_set_worksheet_2_as_default_for_games"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0019_game_has_worksheet_and_class"))
    Game = new_state.apps.get_model("aimmo", "Game")
    assert Game._meta.get_field("game_class").verbose_name == "Class"


@pytest.mark.django_db
def test_worksheet_is_required_and_not_empty(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0018_set_worksheet_2_as_default_for_games"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0019_game_has_worksheet_and_class"))
    Game = new_state.apps.get_model("aimmo", "Game")
    worksheet_field = Game._meta.get_field("worksheet")
    assert not worksheet_field.null
    assert not worksheet_field.blank
