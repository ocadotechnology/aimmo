from django.db import migrations, models
import django.db.models.deletion


def populate_created_by(apps, schema_editor):
    Game = apps.get_model("aimmo", "Game")
    db_alias = schema_editor.connection.alias
    games = Game.objects.using(db_alias).all()
    game_owners = [game.owner for game in games]
    for game_owner in game_owners:
        game_owners_games = Game.objects.filter(owner=game_owner)
        if not game_owners_games[0].created_by:
            game_owners_games.update(created_by=game_owner)
            game_owners_games.save()


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0027_class_created_by"),
        ("aimmo", "0029_game_created_by"),
    ]

    operations = [
        migrations.RunPython(populate_created_by),
    ]
