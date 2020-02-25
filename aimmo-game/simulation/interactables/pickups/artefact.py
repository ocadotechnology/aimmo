from simulation.interactables.conditions import avatar_on_cell, pickup_action_applied
from simulation.interactables.effects import ArtefactEffect
from simulation.interactables.interactable import _Interactable


class Artefact(_Interactable):
    def __init__(self, cell):
        super(Artefact, self).__init__(cell)
        self.delete_after_effects_applied = True
        self.pickup_action_applied = False
        self.conditions = [avatar_on_cell, pickup_action_applied]
        self.effects.append(ArtefactEffect)
        self._in_backpack = False

    def get_targets(self):
        return [self.cell.avatar]

    def __repr__(self):
        return "Artefact(Location={})".format(self.cell.location)

    def serialize(self):
        serialized_artefact = {"type": "artefact"}

        if not self._in_backpack:
            serialized_artefact["location"] = {
                "x": self.cell.location.x,
                "y": self.cell.location.y,
            }

        return serialized_artefact
