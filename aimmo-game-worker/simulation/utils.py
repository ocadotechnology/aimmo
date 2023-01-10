from typing import TypeVar, List

from .errors import NoNearbyArtefactsError


T = TypeVar("T")


class NearbyArtefactsList(List[T]):
    """
    A list-like object that raises NoNearbyArtefactsError when trying to access an element and the list is empty.
    """

    def __getitem__(self, i):
        try:
            return super().__getitem__(i)
        except IndexError:
            if len(self) == 0:
                raise NoNearbyArtefactsError(
                    "The code cannot execute while there aren't any artefacts near. You need to move closer!"
                ) from None
            else:
                raise
