"""
Gets the worksheet we are on and all the configuration that goes with it
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from simulation.game_logic.map_updaters import PickupUpdater
from simulation.interactables.interactable import _Interactable
from simulation.interactables.pickups import (
    YellowOrbArtefact,
    ChestArtefact,
    KeyArtefact,
)
from .avatar_state_serializers import (
    worksheet1_avatar_state_serializer,
    worksheet2_avatar_state_serializer,
    worksheet3_avatar_state_serializer,
)

if TYPE_CHECKING:
    from typing import List, Callable, Dict, NewType
    from simulation.avatar.avatar_wrapper import AvatarWrapper
    from simulation.game_logic.map_updaters import _MapUpdater

    AvatarStateSerializer = NewType(
        "AvatarStateSerializer", Callable[[AvatarWrapper], Dict]
    )


@dataclass
class WorksheetData:
    worksheet_id: int
    era: str
    map_updaters: "List[_MapUpdater]"
    number_of_obstacle_textures: int
    avatar_state_serializer: AvatarStateSerializer = worksheet1_avatar_state_serializer


worksheets = {
    1: WorksheetData(
        worksheet_id=1,
        era="future",
        map_updaters=[PickupUpdater(pickup_types=[YellowOrbArtefact])],
        number_of_obstacle_textures=1,
        avatar_state_serializer=worksheet1_avatar_state_serializer,
    ),
    2: WorksheetData(
        worksheet_id=2,
        era="future",
        map_updaters=[PickupUpdater(pickup_types=[YellowOrbArtefact])],
        number_of_obstacle_textures=1,
        avatar_state_serializer=worksheet2_avatar_state_serializer,
    ),
    3: WorksheetData(
        worksheet_id=3,
        era="ancient",
        map_updaters=[PickupUpdater(pickup_types=[ChestArtefact, KeyArtefact])],
        number_of_obstacle_textures=1,
        avatar_state_serializer=worksheet3_avatar_state_serializer,
    ),
}


def get_worksheet_data() -> WorksheetData:
    worksheet_id = int(os.environ.get("worksheet_id", 1))
    return worksheets.get(worksheet_id, worksheets[1])
