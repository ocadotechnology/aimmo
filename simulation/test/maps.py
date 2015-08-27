from simulation import world_map


class InfiniteMap(world_map.WorldMap):
    def __init__(self):
        pass

    def can_move_to(self, target_location):
        return True

    def get_cell(self, location):
        return world_map.Cell(location)

class EmptyMap(world_map.WorldMap):
    def __init__(self):
        pass
    
    def can_move_to(self, target_location):
        return False

    def get_cell(self, location):
        return world_map.Cell(location)


class ScoreOnOddColumnsMap(InfiniteMap):
    def get_cell(self, location):
        if location.x % 2 == 0:
            return world_map.Cell(location)
        else:
            return world_map.Cell(location, can_move_to=True, generates_score=True)
