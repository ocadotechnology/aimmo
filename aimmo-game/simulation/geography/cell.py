from simulation.action import MoveAction


class Cell(object):
    """
    Any position on the world grid.
    """

    def __init__(self, location, habitable=True, generates_score=False):
        self.location = location
        self.habitable = habitable
        self.generates_score = generates_score
        self.avatar = None
        self.pickup = None
        self.actions = []

        # Used to update the map features in the current view of the user (score points on pickups).
        self.remove_from_scene = None
        self.add_to_scene = None

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={}'.format(
            self.location, self.habitable, self.generates_score, self.avatar, self.pickup)

    def __eq__(self, other):
        return self.location == other.location

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.location)

    @property
    def moves(self):
        return [move for move in self.actions if isinstance(move, MoveAction)]

    @property
    def is_occupied(self):
        return self.avatar is not None

    def serialise(self):
        return {
            'avatar': self.avatar.serialise() if self.avatar else None,
            'generates_score': self.generates_score,
            'habitable': self.habitable,
            'location': self.location.serialise(),
            'pickup': self.pickup.serialise() if self.pickup else None,
        }
