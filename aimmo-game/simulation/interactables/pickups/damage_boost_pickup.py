from simulation.interactables.conditions import avatar_on_cell
from simulation.interactables.effects import DamageBoostEffect
from simulation.interactables.interactable import _Interactable


class DamageBoostPickup(_Interactable):
    def __init__(self, cell):
        super(DamageBoostPickup, self).__init__(cell)
        self.temporary = True

        self.conditions.append(avatar_on_cell)
        self.effects.append(DamageBoostEffect)

    def get_targets(self):
        return [self.cell.avatar]

    def __repr__(self):
        return "DamageBoostPickup(Location={})".format(self.cell.location)

    def serialize(self):
        return {
            "type": "damage_boost",
            "location": {"x": self.cell.location.x, "y": self.cell.location.y},
        }
