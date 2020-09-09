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
            game.worksheet = worksheet2.id

    dependencies = [
        ("aimmo", "0016_game_class"),
    ]

    operations = [migrations.RunPython(set_worksheet_2_as_default_for_games)]


# TODO: write test for this