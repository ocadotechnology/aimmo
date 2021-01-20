from django.core.exceptions import ValidationError
from aimmo.models import Worksheet
from django.contrib.auth.models import User
import pytest

from aimmo import app_settings
from aimmo.forms import AddGameForm
from aimmo.models import Worksheet
from common.models import Class, Teacher
from common.tests.utils.classes import create_class_directly
from common.tests.utils.teacher import signup_teacher_directly

app_settings.GAME_SERVER_URL_FUNCTION = lambda game_id: (
    "base %s" % game_id,
    "path %s" % game_id,
)
app_settings.GAME_SERVER_PORT_FUNCTION = lambda game_id: 0
app_settings.GAME_SERVER_SSL_FLAG = True


@pytest.fixture
def teacher1_email(db) -> str:
    email, _ = signup_teacher_directly()
    return email


@pytest.fixture
def class1(db, teacher1_email) -> Class:
    klass, _, _ = create_class_directly(teacher1_email)
    return klass


@pytest.fixture
def worksheet(db) -> Worksheet:
    return Worksheet.objects.create(name="Test worksheet", starter_code="Trout")


def test_create_game(class1: Class):
    form = AddGameForm(
        Class.objects.all(),
        data={"game_class": class1.id},
    )
    assert form.is_valid()

    game = form.save()
    assert game.game_class == class1
    assert game.worksheet.id == 1


@pytest.mark.django_db
def test_form_with_non_existing_class():
    form = AddGameForm(
        Class.objects.all(),
        data={"game_class": 12345},
    )
    assert not form.is_valid()


@pytest.mark.django_db
def test_cannot_create_duplicate_game(class1: Class):
    # Create first game
    form = AddGameForm(
        Class.objects.all(),
        data={"game_class": class1.id},
    )
    _ = form.save()

    # Create second game with the same class
    form = AddGameForm(
        Class.objects.all(),
        data={"game_class": class1.id},
    )

    assert not form.is_valid()
    assert "Game with this Class already exists." in (
        message for errors in form.errors.values() for message in errors
    )


@pytest.mark.django_db
def test_cannot_add_game_for_classes_not_given_to_form(
    class1: Class, worksheet: Worksheet, teacher1_email: str
):
    # Make query set for form
    class_query_set = Class.objects.filter(id=class1.id)

    # Create class not in the query set
    klass, _, _ = create_class_directly(teacher1_email)

    form = AddGameForm(
        class_query_set,
        data={"game_class": klass.id, "worksheet": worksheet.id},
    )

    assert not form.is_valid()
