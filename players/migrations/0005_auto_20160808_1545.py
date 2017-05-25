# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('players', '0004_auto_20160808_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_number', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='generator',
            field=models.CharField(default=b'Main', max_length=20, choices=[(b'Main', b'Open World'), (b'Level1', b'Level 1')]),
        ),
        migrations.AddField(
            model_name='game',
            name='main_user',
            field=models.ForeignKey(related_name='games_for_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='owner',
            field=models.ForeignKey(related_name='owned_games', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='levelattempt',
            name='game',
            field=models.OneToOneField(to='players.Game'),
        ),
        migrations.AddField(
            model_name='levelattempt',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='levelattempt',
            unique_together=set([('level_number', 'user')]),
        ),
    ]
