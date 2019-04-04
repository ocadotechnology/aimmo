# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("aimmo", "0006_game_static_data")]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="pickup_spawn_chance",
            field=models.FloatField(default=0.1),
        ),
        migrations.AlterField(
            model_name="game",
            name="score_despawn_chance",
            field=models.FloatField(default=0.05),
        ),
        migrations.AlterField(
            model_name="game",
            name="start_height",
            field=models.IntegerField(default=31),
        ),
        migrations.AlterField(
            model_name="game", name="start_width", field=models.IntegerField(default=31)
        ),
        migrations.AlterField(
            model_name="game",
            name="target_num_pickups_per_avatar",
            field=models.FloatField(default=1.2),
        ),
    ]
