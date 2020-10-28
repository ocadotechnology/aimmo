# Generated by Django 2.0 on 2020-10-28 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aimmo', '0021_add_pdf_names_to_worksheet'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='levelattempt',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='levelattempt',
            name='game',
        ),
        migrations.RemoveField(
            model_name='levelattempt',
            name='user',
        ),
        migrations.DeleteModel(
            name='LevelAttempt',
        ),
    ]
