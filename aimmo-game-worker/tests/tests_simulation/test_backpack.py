from collections import namedtuple
import pytest

from simulation.backpack import Backpack

Artefact = namedtuple("Artefact", "type")


@pytest.fixture
def keyboard_artefact():
    return Artefact("keyboard")


@pytest.fixture
def phone_artefact():
    return Artefact("phone")


@pytest.fixture
def coins_artefact():
    return Artefact("coins")


@pytest.fixture
def orb_artefact():
    return Artefact("orb")


@pytest.fixture
def empty_backpack():
    return Backpack()


@pytest.fixture
def backpack(keyboard_artefact, phone_artefact, coins_artefact):
    return Backpack(
        [keyboard_artefact, keyboard_artefact, phone_artefact, coins_artefact, phone_artefact, coins_artefact]
    )


def test_backpack_find(empty_backpack, backpack, keyboard_artefact, phone_artefact, coins_artefact, orb_artefact):
    assert empty_backpack.find("test") == -1
    assert backpack.find(keyboard_artefact.type) == 0
    assert backpack.find(phone_artefact.type) == 2
    assert backpack.find(coins_artefact.type) == 3
    assert backpack.find(orb_artefact.type) == -1
