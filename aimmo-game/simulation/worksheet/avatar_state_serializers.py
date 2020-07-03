from __future__ import annotations

from typing import Dict, Any

from simulation.avatar.avatar_wrapper import AvatarWrapper
import simulation.worksheet.worksheet as worksheet


def _worksheet1_avatar_state_serializer(
    avatar: AvatarWrapper, worksheet: worksheet.WorksheetData
) -> Dict:
    return {
        "health": avatar.health,
        "location": avatar.location.serialize(),
        "id": avatar.player_id,
        "orientation": avatar.orientation,
    }


def _worksheet2_avatar_state_serializer(
    avatar: AvatarWrapper, worksheet: worksheet.WorksheetData
) -> Dict:
    return {
        "health": avatar.health,
        "location": avatar.location.serialize(),
        "score": avatar.score,
        "id": avatar.player_id,
        "orientation": avatar.orientation,
        "backpack": [artefact.serialize() for artefact in avatar.backpack],
    }


worksheet_id_to_avatar_state_serializer: Dict[int, Any] = {
    "1": _worksheet1_avatar_state_serializer,
    "2": _worksheet2_avatar_state_serializer,
}
