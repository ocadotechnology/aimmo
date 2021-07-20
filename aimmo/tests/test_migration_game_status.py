import pytest


@pytest.mark.django_db
def test_game_status_field_added(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0008_default_public_field"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0009_add_game_status"))
    model = new_state.apps.get_model("aimmo", "Game")

    assert model._meta.get_field("status").get_internal_type() == "CharField"
