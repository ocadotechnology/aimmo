from simulation.world_map import WorldMap
from simulation.cell import Cell
from typing import List


def avatar_on_cell(cell: Cell):
    """ Returns an expression that checks if an avatar is on a specified cell """
    def condition(worldmap: WorldMap):
        return cell.avatar is not None
    return condition

def avatar_on_cell_group(cells: List[Cell]):
    """ Returns an expression to check if an avatar exists in a group of cells """
    def condition(worldmap: WorldMap):
        return any([cell.avatar is not None for cell in cells])
    return condition

def avatar_on_team(avatar: object, team):  # TEAMS NOT IMPLENTED, DO NOT USE
    """ Returns an expression that checks if a given avatar is on a specific team """
    def condition(worldmap: WorldMap):
        return avatar.team == team
    return condition

def avatar_has_score(avatar:object, score):  # SCORES NOT IMPLENTED, DO NOT USE
    """ Returns an expression that checks if a given avatar has reached a certain score """
    def condition(worldmap: WorldMap):
        return avatar.score >= score
    return condition

def passive():
    """ For an effect that is applied as long as the object exists, DO NOT USE LIGHTlY """
    def condition(worldmap: WorldMap):
        return True
    return condition
