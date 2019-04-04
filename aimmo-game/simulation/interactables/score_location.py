from simulation.interactables.conditions import avatar_on_cell
from simulation.interactables.effects import ScoreEffect
from simulation.interactables.interactable import _Interactable


class ScoreLocation(_Interactable):
    def __init__(self, cell):
        super(ScoreLocation, self).__init__(cell)

        self.conditions.append(avatar_on_cell)
        self.effects.append(ScoreEffect)

    def get_targets(self):
        return [self.cell.avatar]

    def __repr__(self):
        return f"ScoreLocation(Location={self.cell.location})"

    def serialize(self):
        return {
            "type": "score",
            "location": {"x": self.cell.location.x, "y": self.cell.location.y},
        }
