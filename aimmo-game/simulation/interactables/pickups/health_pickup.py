from simulation.interactables.conditions import avatar_on_cell
from simulation.interactables.effects import HealthEffect
from simulation.interactables.interactable import _Interactable


class HealthPickup(_Interactable):
    def __init__(self, cell):
        super(HealthPickup, self).__init__(cell)
        self.delete_after_effects_applied = True

        self.conditions.append(avatar_on_cell)
        self.effects.append(HealthEffect)

    def get_targets(self):
        return [self.cell.avatar]

    def __repr__(self):
        return "HealthPickup(Location={})".format(self.cell.location)

    def serialize(self):
        return {
            "type": "health",
            "location": {"x": self.cell.location.x, "y": self.cell.location.y},
        }
