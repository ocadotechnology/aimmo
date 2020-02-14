from typing import TYPE_CHECKING

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


def pickup_action_applied(turn_state: TurnState):
    """
    Checks if the interactable has had the `PickupAction` applied to it.

    The `pickup_action_applied` should be set to True by the `PickupAction`.
    """
    try:
        return turn_state.interactable_cell.interactable.pickup_action_applied
    except Exception:
        return False
