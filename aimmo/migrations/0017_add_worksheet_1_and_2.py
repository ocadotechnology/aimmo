from django.db import migrations


class Migration(migrations.Migration):
    def add_worksheet_1_and_2(apps, schema_editor):
        starter_code = """def next_turn(world_state, avatar_state):
    new_dir = direction.NORTH
    # Your code goes here
    action = MoveAction(new_dir)
    return action
"""
        Worksheet = apps.get_model("aimmo", "Worksheet")
        worksheet1 = Worksheet.objects.create(
            name="Present Day I: The Museum", starter_code=starter_code
        )
        worksheet2 = Worksheet.objects.create(
            name="Present Day II", starter_code=starter_code
        )
        worksheet1.save()
        worksheet2.save()

    def remove_worksheets(apps, schema_editor):
        Worksheet = apps.get_model("aimmo", "Worksheet")
        Worksheet.objects.all().delete()

    dependencies = [
        ("aimmo", "0016_game_class"),
    ]

    operations = [
        migrations.RunPython(add_worksheet_1_and_2, reverse_code=remove_worksheets)
    ]
