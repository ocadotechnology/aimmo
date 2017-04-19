# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import players.models


def move_data(apps, schema_editor):
    Player = apps.get_model("players", "Player")
    Avatar = apps.get_model("players", "Avatar")
    Game = apps.get_model("players", "Game")

    if Avatar.objects.count() == 0:
        return
    main_game = Game(pk=1, name="main")
    main_game.save()

    avatars = [Avatar(game=main_game, owner=player.user, code=player.code)
               for player in Player.objects.all()]
    Avatar.objects.bulk_create(avatars)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('players', '0002_auto_20160601_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.TextField()),
                ('auth_token', models.CharField(default=players.models.generate_auth_token, max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('auth_token', models.CharField(default=players.models.generate_auth_token, max_length=24)),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.AddField(
            model_name='avatar',
            name='game',
            field=models.ForeignKey(to='players.Game'),
        ),
        migrations.AddField(
            model_name='avatar',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='avatar',
            unique_together=set([('owner', 'game')]),
        ),
        migrations.RunPython(move_data),
        migrations.DeleteModel(
            name='Player',
        ),
    ]
