from .artefact import Artefact


class ChestArtefact(Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "chest"
