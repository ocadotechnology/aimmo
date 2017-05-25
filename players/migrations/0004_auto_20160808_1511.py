# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_auto_20160802_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='obstacle_ratio',
            field=models.FloatField(default=0.1),
        ),
        migrations.AddField(
            model_name='game',
            name='pickup_spawn_chance',
            field=models.FloatField(default=0.02),
        ),
        migrations.AddField(
            model_name='game',
            name='score_despawn_chance',
            field=models.FloatField(default=0.02),
        ),
        migrations.AddField(
            model_name='game',
            name='start_height',
            field=models.IntegerField(default=11),
        ),
        migrations.AddField(
            model_name='game',
            name='start_width',
            field=models.IntegerField(default=11),
        ),
        migrations.AddField(
            model_name='game',
            name='target_num_cells_per_avatar',
            field=models.FloatField(default=16),
        ),
        migrations.AddField(
            model_name='game',
            name='target_num_pickups_per_avatar',
            field=models.FloatField(default=0.5),
        ),
        migrations.AddField(
            model_name='game',
            name='target_num_score_locations_per_avatar',
            field=models.FloatField(default=0.5),
        ),
    ]
