from unittest.mock import patch

from simulation.game_logic import PickupUpdater
from simulation.interactables.pickups import YellowOrbArtefact
from simulation.worksheet.avatar_state_serializers import (
    worksheet1_avatar_state_serializer,
    worksheet2_avatar_state_serializer,
)
from simulation.worksheet.worksheet import get_worksheet_data


def test_default_worksheet_loaded_when_no_worksheet_id_provided():
    worksheet = get_worksheet_data()
    assert worksheet.era == "future"
    assert len(worksheet.map_updaters) == 1
    assert type(worksheet.map_updaters[0]) == PickupUpdater
    assert worksheet.map_updaters[0].pickup_types == [YellowOrbArtefact]
    assert worksheet.avatar_state_serializer == worksheet1_avatar_state_serializer


def test_worksheet_loads_from_environment_variables():
    with patch.dict("os.environ", values={"worksheet_id": "2"}):
        worksheet = get_worksheet_data()
        assert worksheet.era == "future"
        assert len(worksheet.map_updaters) == 1
        assert type(worksheet.map_updaters[0]) == PickupUpdater
        assert worksheet.map_updaters[0].pickup_types == [YellowOrbArtefact]
        assert worksheet.avatar_state_serializer == worksheet2_avatar_state_serializer
