import pytest


@pytest.mark.django_db
def test_generate_auth_token_for_games(migrator):
    old_state = migrator.apply_initial_migration(("aimmo", "0024_unique_class_per_game"))

    Game = old_state.apps.get_model("aimmo", "Game")
    game = Game.objects.create()
    game.save()
    game_id = game.id

    new_state = migrator.apply_tested_migration(("aimmo", "0025_generate_auth_token"))

    Game = new_state.apps.get_model("aimmo", "Game")
    game = Game.objects.get(id=game_id)
    assert game.auth_token is not None and game.auth_token != ""


@pytest.mark.django_db
def test_clear_auth_token_for_games(migrator):
    old_state = migrator.apply_initial_migration(("aimmo", "0025_generate_auth_token"))

    Game = old_state.apps.get_model("aimmo", "Game")
    game = Game.objects.create()
    game.save()
    game_id = game.id

    new_state = migrator.apply_tested_migration(("aimmo", "0024_unique_class_per_game"))

    Game = new_state.apps.get_model("aimmo", "Game")
    game = Game.objects.get(id=game_id)
    assert game.auth_token == ""
