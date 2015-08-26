from simulation import world_map


class InfiniteMap(world_map.WorldMap):
    def __init__(self):
        pass

    def can_move_to(self, target_location):
        return True


class EmptyMap(world_map.WorldMap):
    def __init__(self):
        pass
    
    def can_move_to(self, target_location):
        return False
