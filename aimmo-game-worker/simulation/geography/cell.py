from simulation.avatar.avatar_state import AvatarState
from simulation.geography.location import Location


class Cell(object):

    """
    Any position on the world grid.
    """

    def __init__(self, location, avatar=None, **kwargs):
        self.location = Location(**location)
        if avatar:
            self.avatar = AvatarState(**avatar)
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return 'Cell({} h={} a={} p={})'.format(
            self.location,
            getattr(self, 'habitable', 0),
            getattr(self, 'avatar', 0),
            getattr(self, 'pickup', 0))

    def __eq__(self, other):
        return self.location == other.location

    def __ne__(self, other):
        return not self == other

