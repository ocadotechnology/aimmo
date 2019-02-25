from simulation.cell import Cell
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.world_map import WorldMap

def avatar_on_cell(cell: Cell):
    """ Returns an expression that checks if an avatar is on a specified cell """
    def condition(worldmap: 'WorldMap'):
        return cell.avatar is not None
    return condition


def passive():
    """ For an effect that is applied as long as the object exists, DO NOT USE LIGHTlY """
    def condition(worldmap: 'WorldMap'):
        return True
    return condition
