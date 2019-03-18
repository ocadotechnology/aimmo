

def serialize_interactables(world_map):
    return [cell.interactable.serialize() for cell in world_map.interactable_cells()]
