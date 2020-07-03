"""
Gets the worksheet we are on and all the configuration that goes with it
"""

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .game_logic.map_updaters import PickupUpdater

if TYPE_CHECKING:
    from typing import List
    from .game_logic.map_updaters import _MapUpdater


@dataclass
class WorksheetData:
    era: str
    map_updaters: "List[_MapUpdater]"


ERA_CHOICES = {
    1: "future",
    2: "ancient",
    3: "modern day",
    4: "prehistoric",
    5: "broken future",
}


_worksheet_id_to_map_updaters = {1: [PickupUpdater]}


def get_worksheet_data() -> WorksheetData:
    worksheet_id = os.environ.get("worksheet_id", 1)
    map_updaters = _worksheet_id_to_map_updaters.get(worksheet_id, [])
    era_id = os.environ.get("era", "1")
    return WorksheetData(era=ERA_CHOICES[int(era_id)], map_updaters=map_updaters)


WORKSHEET = get_worksheet_data()
