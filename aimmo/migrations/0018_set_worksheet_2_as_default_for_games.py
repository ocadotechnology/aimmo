from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aimmo", "0017_add_worksheet_1_and_2"),
    ]

    def set_worksheet_2_as_default_for_games(apps, schema_editor):
        Worksheet = apps.get_model("aimmo", "Worksheet")
        Game = apps.get_model("aimmo", "Game")
        worksheet2 = Worksheet.objects.get(name="Present Day II")
        games_with_no_worksheet = Game.objects.filter(worksheet=None)
        for game in games_with_no_worksheet:
            game.worksheet = worksheet2
            game.save()

    def dummy_reverse(apps, schema_editor):
        """It's not possible to reverse this data migration
        but we want to allow Django to reverse previous migrations.
        """
        pass

    operations = [
        migrations.RunPython(
            set_worksheet_2_as_default_for_games, reverse_code=dummy_reverse
        )
    ]
