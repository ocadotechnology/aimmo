from .artefact import Artefact


class KeyArtefact(Artefact):
    def __init__(self, cell):
        super().__init__(cell)
        self._type = "key"
