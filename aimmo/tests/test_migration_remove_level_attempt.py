import pytest


@pytest.mark.django_db
def test_level_attempt_model_removed(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0022_allow_games_to_have_no_name"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0023_remove_level_attempt"))
    model_names = [model._meta.db_table for model in new_state.apps.get_models()]
    assert "aimmo_levelattempt" not in model_names
