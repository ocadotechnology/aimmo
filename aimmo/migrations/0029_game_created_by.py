# Generated by Django 3.2.15 on 2022-10-05 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0028_coding_club_downloads'),
        ('aimmo', '0028_manygames'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_created_by_teacher', to='common.teacher'),
        ),
    ]
