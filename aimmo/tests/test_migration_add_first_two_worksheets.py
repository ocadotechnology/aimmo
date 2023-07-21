import pytest


@pytest.mark.django_db
def test_first_two_worksheets_added(migrator):
    migrator.apply_initial_migration(("aimmo", "0016_game_class"))
    new_state = migrator.apply_tested_migration(("aimmo", "0017_add_worksheet_1_and_2"))
    Worksheet = new_state.apps.get_model("aimmo", "Worksheet")
    all_worksheets = Worksheet.objects.all()

    assert all_worksheets.count() == 2


@pytest.mark.django_db
def test_no_worksheets_after_rollback(migrator):
    migrator.apply_initial_migration(("aimmo", "0017_add_worksheet_1_and_2"))
    new_state = migrator.apply_tested_migration(("aimmo", "0016_game_class"))
    Worksheet = new_state.apps.get_model("aimmo", "Worksheet")
    all_worksheets = Worksheet.objects.all()

    assert all_worksheets.count() == 0


@pytest.mark.django_db
def test_worksheet_2_is_default_for_games_without_one(migrator):
    old_state = migrator.apply_initial_migration(
        ("aimmo", "0017_add_worksheet_1_and_2"),
    )
    Game = old_state.apps.get_model("aimmo", "Game")
    Worksheet = old_state.apps.get_model("aimmo", "Worksheet")
    worksheet1 = Worksheet.objects.get(name="Present Day I: The Museum")
    game_with_worksheet = Game.objects.create(name="game with worksheet before migration", worksheet=worksheet1)
    game_with_worksheet.save()
    game_without_worksheet = Game.objects.create(name="game without worksheet before migration")
    game_without_worksheet.save()
    assert game_without_worksheet.worksheet is None

    new_state = migrator.apply_tested_migration(("aimmo", "0018_set_worksheet_2_as_default_for_games"))
    Game = new_state.apps.get_model("aimmo", "Game")
    Worksheet = new_state.apps.get_model("aimmo", "Worksheet")
    worksheet2 = Worksheet.objects.get(name="Present Day II")
    game_with_worksheet = Game.objects.get(name="game with worksheet before migration")
    game_without_worksheet = Game.objects.get(name="game without worksheet before migration")
    assert game_with_worksheet.worksheet is not None
    assert game_without_worksheet.worksheet is not None
    assert game_with_worksheet.worksheet.name == "Present Day I: The Museum"
    assert game_without_worksheet.worksheet.name == "Present Day II"
