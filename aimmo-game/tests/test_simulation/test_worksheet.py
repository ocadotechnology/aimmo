from unittest.mock import patch

from simulation.game_logic import PickupUpdater
from simulation.worksheet.avatar_state_serializers import (
    worksheet_id_to_avatar_state_serializer,
)
from simulation.worksheet.worksheet import get_worksheet_data


def test_default_worksheet_loaded_when_no_worksheet_id_provided():
    worksheet = get_worksheet_data()
    assert worksheet.era == "future"
    assert worksheet.map_updaters == [PickupUpdater]
    assert (
        worksheet.avatar_state_serializer
        == worksheet_id_to_avatar_state_serializer["1"]
    )


def test_worksheet_loads_from_environment_variables():
    with patch.dict("os.environ", values={"worksheet_id": "2", "era": "3"}):
        worksheet = get_worksheet_data()
        assert worksheet.era == "modern day"
        assert worksheet.map_updaters == [PickupUpdater]
        assert (
            worksheet.avatar_state_serializer
            == worksheet_id_to_avatar_state_serializer["2"]
        )
