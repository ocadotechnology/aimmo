from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from simulation.game_state import GameState
    from simulation.cell import Cell


class TurnState:
    """
    Data structure used by conditions.

    On a given turn, all conditions for a pickup get access to the same TurnState object.
    """

    def __init__(self, game_state: "GameState", interactable_cell: "Cell"):
        self.game_state = game_state
        self.interactable_cell = interactable_cell


def avatar_on_cell(turn_state: TurnState):
    """ Returns an expression that checks if an avatar is on a specified cell. """
    return turn_state.interactable_cell.avatar is not None
