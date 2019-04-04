# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models, transaction, IntegrityError

import aimmo.models


def migrate_data_forward(apps, schema_editor):
    Player = apps.get_model("aimmo", "Player")
    Avatar = apps.get_model("aimmo", "Avatar")
    Game = apps.get_model("aimmo", "Game")

    if Player.objects.count() == 0:
        return
    main_game = Game(pk=1, name="main")
    main_game.save()

    avatars = [
        Avatar(game=main_game, owner=player.user, code=player.code)
        for player in Player.objects.all()
    ]
    Avatar.objects.bulk_create(avatars)


def migrate_data_backward(apps, schema_editor):
    Player = apps.get_model("aimmo", "Player")
    Avatar = apps.get_model("aimmo", "Avatar")

    if Avatar.objects.count() == 0:
        return
    for avatar in Avatar.objects.all():
        player = Player(user=avatar.owner, code=avatar.code)
        try:
            with transaction.atomic():
                player.save()
        except IntegrityError:
            # Stuff doesn't map as can have more than one Avatar but only one Player
            pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("aimmo", "0002_auto_20160601_1914"),
    ]

    operations = [
        migrations.CreateModel(
            name="Avatar",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("code", models.TextField()),
                (
                    "auth_token",
                    models.CharField(
                        default=aimmo.models.generate_auth_token, max_length=24
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "auth_token",
                    models.CharField(
                        default=aimmo.models.generate_auth_token, max_length=24
                    ),
                ),
                ("public", models.BooleanField(default=True)),
                (
                    "can_play",
                    models.ManyToManyField(
                        related_name="playable_games", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        related_name="owned_games",
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="avatar", name="game", field=models.ForeignKey(to="aimmo.Game")
        ),
        migrations.AddField(
            model_name="avatar",
            name="owner",
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name="avatar", unique_together=set([("owner", "game")])
        ),
        migrations.RunPython(migrate_data_forward, migrate_data_backward),
        migrations.RemoveField(model_name="player", name="user"),
        migrations.DeleteModel(name="Player"),
    ]
