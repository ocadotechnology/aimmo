from collections import namedtuple
from multiprocessing.sharedctypes import Value
from typing import TypeVar, List

T = TypeVar("T")


class Backpack(List[T]):
    """
    A list of artefacts that has a `find` method to find the index of an artefact type.
    """

    def find(self, artefact_type: str) -> int:
        """
        Finds an artefact of type `artefact_type` and returns its index or -1 if there's no artefact of that type.

        Args:
            artefact_type: The type of artefact to find.

        Returns:
            The index of the artefact or -1 if it doesn't exist.
        """
        return next((i for i, artefact in enumerate(self) if artefact.type == artefact_type), -1)
