from simulation.interactables.conditions import avatar_on_cell, in_backpack
from simulation.interactables.effects import ArtefactEffect
from simulation.interactables.interactable import _Interactable


class _Artefact(_Interactable):
    """
    Base artefact class. self._type should be overridden in __init__.
    """

    def __init__(self, cell):
        super().__init__(cell)
        self.delete_after_effects_applied = True
        self.in_backpack = False
        self.conditions = [avatar_on_cell, in_backpack]
        self.effects.append(ArtefactEffect)
        self._type = "_artefact"

    def get_targets(self):
        return [self.cell.avatar]

    def __str__(self):
        return self._type

    def __repr__(self):
        return f"{type(self).__name__}(Location={self.cell.location})"

    def serialize(self):
        serialized_artefact = {"type": self._type}

        if not self.in_backpack:
            serialized_artefact["location"] = {
                "x": self.cell.location.x,
                "y": self.cell.location.y,
            }

        return serialized_artefact


class ChestArtefact(_Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "chest"


class KeyArtefact(_Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "key"


class YellowOrbArtefact(_Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "yellow_orb"


class PhoneArtefact(_Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "phone"


class KeyboardArtefact(_Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "keyboard"


class CoinsArtefact(_Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "coins"
