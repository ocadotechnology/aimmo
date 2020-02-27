from simulation.interactables.conditions import avatar_on_cell, in_backpack
from simulation.interactables.effects import ArtefactEffect
from simulation.interactables.interactable import _Interactable


class Artefact(_Interactable):
    def __init__(self, cell):
        super(Artefact, self).__init__(cell)
        self.delete_after_effects_applied = True
        self.in_backpack = False
        self.conditions = [avatar_on_cell, in_backpack]
        self.effects.append(ArtefactEffect)

    def get_targets(self):
        return [self.cell.avatar]

    def __repr__(self):
        return "Artefact(Location={})".format(self.cell.location)

    def serialize(self):
        serialized_artefact = {"type": "artefact"}

        if not self.in_backpack:
            serialized_artefact["location"] = {
                "x": self.cell.location.x,
                "y": self.cell.location.y,
            }

        return serialized_artefact
