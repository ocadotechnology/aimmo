import pytest

from simulation.errors import NoNearbyArtefactsError
from simulation.location import Location
from simulation.utils import NearbyArtefactsList
from simulation.world_map import ARTEFACT_TYPES, WorldMapCreator


@pytest.fixture
def avatar_state_json():
    return {"location": {"x": 0, "y": 0}, "backpack": [{"type": "key"}]}


def _generate_cells(columns=3, rows=3):
    cells = [
        {
            "location": {"x": x, "y": y},
            "habitable": True,
            "avatar": None,
            "interactable": None,
        }
        for x in range(-columns // 2 + 1, 1 + columns // 2)
        for y in range(-rows // 2 + 1, 1 + rows // 2)
    ]
    return cells


def assertGridSize(map, expected_rows, expected_columns=None):
    if expected_columns is None:
        expected_columns = expected_rows
    assert len(list(map.all_cells())) == expected_rows * expected_columns


def assertLocationsEqual(actual_cells, expected_locations):
    actual_cells = list(actual_cells)
    actual = frozenset(cell.location for cell in actual_cells)
    assert actual == frozenset(expected_locations)
    assert len(actual_cells) == len(list(expected_locations))


def test_grid_size():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells(1, 3))
    assertGridSize(map, 1, 3)


def test_all_cells():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    assertLocationsEqual(
        map.all_cells(),
        [Location(x, y) for x in range(-1, 2) for y in range(-1, 2)],
    )


def test_score_cells():
    cells = _generate_cells()
    cells[0]["interactable"] = {"type": "score"}
    cells[8]["interactable"] = {"type": "score"}
    map = WorldMapCreator.generate_world_map_from_cells_data(cells)
    assertLocationsEqual(map.score_cells(), (Location(-1, -1), Location(1, 1)))


def test_interactable_cells():
    cells = _generate_cells()
    cells[0]["interactable"] = {"type": "health"}
    cells[8]["interactable"] = {"type": "damage_boost"}
    map = WorldMapCreator.generate_world_map_from_cells_data(cells)
    assertLocationsEqual(map.interactable_cells(), (Location(-1, -1), Location(1, 1)))


def test_artefact_cell():
    cells = _generate_cells()
    cells[0]["interactable"] = {"type": ARTEFACT_TYPES[0]}
    map = WorldMapCreator.generate_world_map_from_cells_data(cells)
    assert map.get_cell(Location(-1, -1)).has_artefact() == True


def test_location_is_visible():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    for x in (0, 1):
        for y in (0, 1):
            assert map.is_visible(Location(x, y)) == True


def test_x_off_map_is_not_visible():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    for y in (0, 1):
        assert map.is_visible(Location(-2, y)) == False
        assert map.is_visible(Location(2, y)) == False


def test_y_off_map_is_not_visible():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    for x in (0, 1):
        assert map.is_visible(Location(x, -2)) == False
        assert map.is_visible(Location(x, 2)) == False


def test_get_valid_cell():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    for x in (0, 1):
        for y in (0, 1):
            location = Location(x, y)
            assert map.get_cell(location).location == location


def test_get_x_off_map():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    for y in (0, 1):
        with pytest.raises(KeyError):
            map.get_cell(Location(-2, y))
        with pytest.raises(KeyError):
            map.get_cell(Location(2, y))


def test_get_y_off_map():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    for x in (0, 1):
        with pytest.raises(KeyError):
            map.get_cell(Location(x, -2))
        with pytest.raises(KeyError):
            map.get_cell(Location(x, 2))


def test_can_move_to():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    target = Location(1, 1)
    assert map.can_move_to(target) == True


def test_cannot_move_to_cell_off_grid():
    map = WorldMapCreator.generate_world_map_from_cells_data(_generate_cells())
    target = Location(4, 1)
    assert map.can_move_to(target) == False


def test_cannot_move_to_uninhabitable_cell():
    cells = _generate_cells()
    cells[0]["obstacle"] = {"location": {"x": -1, "y": -1}}
    map = WorldMapCreator.generate_world_map_from_cells_data(cells)
    assert map.can_move_to(Location(-1, -1)) == False


def test_cannot_move_to_inhabited_cell(avatar_state_json):
    cells = _generate_cells()
    cells[1]["avatar"] = avatar_state_json
    map = WorldMapCreator.generate_world_map_from_cells_data(cells)
    assert map.can_move_to(Location(-1, 0)) == False


def test_scan_nearby(avatar_state_json, capsys):
    cells = _generate_cells(5, 5)
    cells[0]["avatar"] = avatar_state_json
    cells[2]["obstacle"] = {"location": {"x": 0, "y": 0}}
    cells[4]["interactable"] = {"type": ARTEFACT_TYPES[-1]}
    map = WorldMapCreator.generate_world_map_from_cells_data(cells)
    artefacts = map.scan_nearby(Location(-1, 0))
    assert type(artefacts) == NearbyArtefactsList
    assert len(artefacts) == 1
    with pytest.raises(IndexError):
        artefacts[1]

    # Test NoNearbyArtefactsError
    artefacts = map.scan_nearby(Location(5, 5), radius=1)
    assert type(artefacts) == NearbyArtefactsList
    assert len(artefacts) == 0
    artefacts[0]
    captured = capsys.readouterr()
    # check the print statement matches
    assert captured.out == "There aren't any nearby artefacts, you need to move closer!\n"
