from simulation.game_logic import PickupUpdater
from simulation.worksheet import get_worksheet_data


def test_default_worksheet_loaded_when_no_worksheet_id_provided():
    worksheet = get_worksheet_data()
    assert worksheet.era == "future"
    assert worksheet.map_updaters == [PickupUpdater]
