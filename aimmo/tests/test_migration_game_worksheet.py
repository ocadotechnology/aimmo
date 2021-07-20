import pytest


@pytest.mark.django_db
def test_game_has_worksheet_as_foreign_key(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0014_add_worksheet_model"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0015_game_worksheet"))
    Worksheet = new_state.apps.get_model("aimmo", "Worksheet")
    Game = new_state.apps.get_model("aimmo", "Game")

    test_worksheet = Worksheet.objects.create(id=1, name="Test", starter_code="code")
    test_worksheet.save()
    test_game = Game.objects.create(id=1, name="test", public=True)
    test_game.worksheet = test_worksheet
    test_game.save()

    assert test_game.worksheet.id == test_worksheet.id
