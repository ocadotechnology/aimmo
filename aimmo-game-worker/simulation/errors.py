class Error(Exception):
    """Base class for other exceptions"""

    pass


class NoNearbyArtefactsError(Error):
    """Raised when there are no nearby artefacts"""

    pass
