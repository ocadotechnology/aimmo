# Generated by Django 2.2.17 on 2021-01-19 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aimmo", "0023_remove_level_attempt"),
    ]

    operations = [
        migrations.RunSQL(
            """
            DELETE
            FROM
                aimmo_game
            WHERE
                id IN (
                SELECT
                    id
                FROM
                    aimmo_game ag
                JOIN (
                    SELECT
                        owner_id,
                        game_class_id,
                        MAX(id) target_game_id
                    FROM
                        aimmo_game
                    GROUP BY
                        owner_id,
                        game_class_id
                    HAVING
                        count(*) > 1) duplicate_game ON
                    ag.owner_id = duplicate_game.owner_id
                    AND ag.game_class_id = duplicate_game.game_class_id
                    AND ag.id != duplicate_game.target_game_id)
            """
        ),
        migrations.AlterField(
            model_name="game",
            name="game_class",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="common.Class",
                verbose_name="Class",
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="worksheet",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="aimmo.Worksheet",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="game",
            unique_together=set(),
        ),
    ]
