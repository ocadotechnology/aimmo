"""
Gets the worksheet we are on and all the configuration that goes with it
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from simulation.game_logic.map_updaters import PickupUpdater
from .avatar_state_serializers import worksheet_id_to_avatar_state_serializer

if TYPE_CHECKING:
    from typing import List, Callable, Dict, NewType
    from simulation.avatar.avatar_wrapper import AvatarWrapper
    from simulation.game_logic.map_updaters import _MapUpdater

    AvatarStateSerializer = NewType(
        "AvatarStateSerializer", Callable[[AvatarWrapper, "WorksheetData"], Dict]
    )


@dataclass
class WorksheetData:
    worksheet_id: int
    era: str
    map_updaters: "List[_MapUpdater]"
    avatar_state_serializer: AvatarStateSerializer = worksheet_id_to_avatar_state_serializer[
        "1"
    ]


ERA_CHOICES = {
    "1": "future",
    "2": "ancient",
    "3": "modern day",
    "4": "prehistoric",
    "5": "broken future",
}


_worksheet_id_to_map_updaters = {"1": [PickupUpdater], "2": [PickupUpdater]}


def get_worksheet_data() -> WorksheetData:
    worksheet_id = os.environ.get("worksheet_id", "1")
    map_updaters = _worksheet_id_to_map_updaters.get(worksheet_id, [])
    avatar_state_serializer: AvatarStateSerializer = worksheet_id_to_avatar_state_serializer[
        worksheet_id
    ]
    era_id = os.environ.get("era", "1")
    return WorksheetData(
        worksheet_id=int(worksheet_id),
        era=ERA_CHOICES[era_id],
        map_updaters=map_updaters,
        avatar_state_serializer=avatar_state_serializer,
    )


WORKSHEET = get_worksheet_data()
