# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aimmo', '0005_auto_20160808_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='static_data',
            field=models.TextField(null=True, blank=True),
        ),
    ]
