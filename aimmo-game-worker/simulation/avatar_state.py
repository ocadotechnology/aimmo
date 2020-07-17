from collections import namedtuple
from simulation.location import Location
from typing import Dict


def create_avatar_state(avatar_state_json: Dict):
    avatar_state_dict = avatar_state_json.copy()
    avatar_state_dict["location"] = Location(**avatar_state_json["location"])
    return namedtuple("AvatarState", avatar_state_dict.keys())(
        *avatar_state_dict.values()
    )
