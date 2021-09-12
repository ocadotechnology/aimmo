import pytest


@pytest.mark.django_db
def test_reset_token(migrator):
    old_state = migrator.apply_initial_migration(
        ("aimmo", "0010_alter_game_token"),
    )
    Game = old_state.apps.get_model("aimmo", "Game")
    game = Game.objects.create(id=1, name="test", public=True)
    game.auth_token = "I'm a token"
    game.save()

    new_state = migrator.apply_tested_migration(("aimmo", "0011_reset_game_tokens"))
    Game = new_state.apps.get_model("aimmo", "Game")
    game = Game.objects.get(id=1)
    assert game.auth_token == ""
