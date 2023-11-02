# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-03-02 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("aimmo", "0011_reset_game_tokens"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="generator",
            field=models.CharField(
                choices=[("Main", "Open World"), ("Level1", "Level 1")],
                default="Main",
                max_length=20,
            ),
        )
    ]
