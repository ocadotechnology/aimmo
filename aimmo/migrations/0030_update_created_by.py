from django.db import migrations, models
import django.db.models.deletion


def populate_created_by(apps, schema_editor):
    Game = apps.get_model("aimmo", "Game")
    Teacher = apps.get_model("common", "Teacher")
    db_alias = schema_editor.connection.alias
    games = Game.objects.using(db_alias).filter(created_by=None)
    [Game.objects.using(db_alias).filter(id=game.id).update(created_by=game.owner) for game in games]


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0027_class_created_by"),
        ("aimmo", "0029_game_created_by"),
    ]

    operations = [
        migrations.RunPython(populate_created_by),
    ]
