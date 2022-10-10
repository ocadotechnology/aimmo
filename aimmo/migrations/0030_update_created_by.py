from django.db import migrations, models
import django.db.models.deletion


def populate_created_by(apps, schema_editor):
    Game = apps.get_model("aimmo", "Game")
    db_alias = schema_editor.connection.alias
    games = Game.objects.using(db_alias).all()
    for game in games:
        if not game.created_by:
            game.created_by = game.owner.new_teacher


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0027_class_created_by"),
        ("aimmo", "0029_game_created_by"),
    ]

    operations = [
        migrations.RunPython(populate_created_by),
    ]
