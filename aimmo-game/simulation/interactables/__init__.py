"""
interactables is a library for adding dynamic objects to the world map.

This contains the definitions of these objects, including all their effects and conditions,
multiple interactbles of the same type are grouped (pickups for example).
"""


def serialize_interactables(world_map):
    return [cell.interactable.serialize() for cell in world_map.interactable_cells()]
