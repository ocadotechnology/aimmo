from simulation.cell import Cell
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.world_map import WorldMap

class TurnState:
    def __init__(self, world_map: 'WorldMap', pickup_cell: Cell):
        self.world_map = world_map
        self.pickup_cell = pickup_cell


def avatar_on_cell(turn_state: TurnState):
    """ Returns an expression that checks if an avatar is on a specified cell """
    return turn_state.pickup_cell.avatar is not None


def passive(turn_state: TurnState):
    """ For an effect that is applied as long as the object exists, DO NOT USE LIGHTlY """
    return True
