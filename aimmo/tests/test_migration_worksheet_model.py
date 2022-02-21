import pytest


@pytest.mark.django_db
def test_worksheet_model_exists(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0013_alter_game_can_play"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0014_add_worksheet_model"))
    model_names = [model._meta.db_table for model in new_state.apps.get_models()]
    assert "aimmo_worksheet" in model_names


@pytest.mark.django_db
def test_worksheet_has_correct_fields(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0013_alter_game_can_play"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0014_add_worksheet_model"))
    model = new_state.apps.get_model("aimmo", "Worksheet")

    assert model._meta.get_field("name").get_internal_type() == "CharField"
    assert (
        model._meta.get_field("era").get_internal_type() == "PositiveSmallIntegerField"
    )
    assert model._meta.get_field("starter_code").get_internal_type() == "TextField"


@pytest.mark.django_db
def test_worksheet_has_new_fields_added(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0019_game_has_worksheet_and_class"),
    )
    new_state = migrator.apply_tested_migration(("aimmo", "0020_add_info_to_worksheet"))
    Worksheet = new_state.apps.get_model("aimmo", "Worksheet")

    assert Worksheet._meta.get_field("description").get_internal_type() == "TextField"
    assert (
        Worksheet._meta.get_field("short_description").get_internal_type()
        == "TextField"
    )
    assert Worksheet._meta.get_field("image_path").get_internal_type() == "CharField"
    assert (
        Worksheet._meta.get_field("active_image_path").get_internal_type()
        == "CharField"
    )
    assert (
        Worksheet._meta.get_field("thumbnail_image_path").get_internal_type()
        == "CharField"
    )
    assert (
        Worksheet._meta.get_field("thumbnail_text").get_internal_type() == "CharField"
    )
    assert Worksheet._meta.get_field("sort_order").get_internal_type() == "IntegerField"


@pytest.mark.django_db
def test_worksheet_has_new_fields_added_two(migrator):
    migrator.apply_initial_migration(
        ("aimmo", "0020_add_info_to_worksheet"),
    )
    new_state = migrator.apply_tested_migration(
        ("aimmo", "0021_add_pdf_names_to_worksheet")
    )
    Worksheet = new_state.apps.get_model("aimmo", "Worksheet")

    assert (
        Worksheet._meta.get_field("teacher_pdf_name").get_internal_type() == "CharField"
    )
    assert (
        Worksheet._meta.get_field("student_pdf_name").get_internal_type() == "CharField"
    )
