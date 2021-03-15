from .artefact import Artefact


class YellowOrbArtefact(Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "yellow_orb"
