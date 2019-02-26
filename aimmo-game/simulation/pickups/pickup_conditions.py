from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.world_map import WorldMap
    from simulation.cell import Cell

class TurnState:
    def __init__(self, world_map: 'WorldMap', pickup_cell: 'Cell'):
        self.world_map = world_map
        self.pickup_cell = pickup_cell


def avatar_on_cell(turn_state: TurnState):
    """ Returns an expression that checks if an avatar is on a specified cell """
    return turn_state.pickup_cell.avatar is not None
