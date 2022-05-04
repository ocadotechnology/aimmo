from __future__ import annotations

from typing import Dict

from simulation.avatar.avatar_wrapper import AvatarWrapper


def worksheet1_avatar_state_serializer(avatar: AvatarWrapper) -> Dict:
    return {
        "location": avatar.location.serialize(),
        "id": avatar.player_id,
        "orientation": avatar.orientation,
    }


def worksheet2_avatar_state_serializer(avatar: AvatarWrapper) -> Dict:
    return {
        "location": avatar.location.serialize(),
        "id": avatar.player_id,
        "orientation": avatar.orientation,
        "backpack": [artefact.serialize() for artefact in avatar.backpack],
    }


def worksheet3_avatar_state_serializer(avatar: AvatarWrapper) -> Dict:
    return {
        "location": avatar.location.serialize(),
        "id": avatar.player_id,
        "orientation": avatar.orientation,
        "backpack": [artefact.serialize() for artefact in avatar.backpack],
    }


def worksheet4_avatar_state_serializer(avatar: AvatarWrapper) -> Dict:
    return {
        "location": avatar.location.serialize(),
        "id": avatar.player_id,
        "orientation": avatar.orientation,
        "backpack": [artefact.serialize() for artefact in avatar.backpack],
    }
