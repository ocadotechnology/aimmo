from simulation import world_map
from simulation.location import Location


class InfiniteMap(world_map.WorldMap):
    def __init__(self):
        pass

    def can_move_to(self, target_location):
        return True

    def all_cells(self):
        yield world_map.Cell(Location(0, 0))

    def get_cell(self, location):
        return world_map.Cell(location)

class EmptyMap(world_map.WorldMap):
    def __init__(self):
        pass
    
    def can_move_to(self, target_location):
        return False

    def all_cells(self):
        return iter(())

    def get_cell(self, location):
        return world_map.Cell(location)


class ScoreOnOddColumnsMap(InfiniteMap):
    def get_cell(self, location):
        if location.x % 2 == 0:
            return world_map.Cell(location)
        else:
            return world_map.Cell(location, habitable=True, generates_score=True)
