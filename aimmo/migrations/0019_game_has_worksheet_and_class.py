# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-09-09 14:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
        ("aimmo", "0018_set_worksheet_2_as_default_for_games"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="game_class",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="games_for_class",
                to="common.Class",
                verbose_name="Class",
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="worksheet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="aimmo.Worksheet"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="game",
            unique_together=set([("game_class", "worksheet")]),
        ),
    ]
