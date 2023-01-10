from typing import TypeVar, List
import warnings

from .errors import NoNearbyArtefactsError
from .warnings import NoNearbyArtefactsWarning


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
                warnings.warn(
                    "There aren't any nearby artefacts, you need to move closer!",
                    NoNearbyArtefactsWarning,
                    stacklevel=2,
                )
            else:
                raise
