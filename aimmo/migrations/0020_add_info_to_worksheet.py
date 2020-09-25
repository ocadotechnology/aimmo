# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-09-25 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aimmo', '0019_game_has_worksheet_and_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheet',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='thumbnail_image_path',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worksheet',
            name='thumbnail_text',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
