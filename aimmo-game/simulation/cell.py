from simulation.action import MoveAction


class Cell(object):
    """
    Any position on the world grid.
    """

    def __init__(self, location, habitable=True, generates_score=False,
                 partially_fogged=False):
        self.location = location
        self.habitable = habitable
        self.generates_score = generates_score
        self.avatar = None
        self.interactable = None
        self.partially_fogged = partially_fogged
        self.actions = []

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={} f{})'.format(
            self.location, self.habitable, self.generates_score, self.avatar, self.interactable,
            self.partially_fogged)

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

    def serialize(self):
        if self.partially_fogged:
            return {
                'generates_score': self.generates_score,
                'location': self.location.serialize(),
                'partially_fogged': self.partially_fogged
            }
        else:
            return {
                'avatar': self.avatar.serialize() if self.avatar else None,
                'generates_score': self.generates_score,
                'habitable': self.habitable,
                'location': self.location.serialize(),
                'pickup': self.interactable.serialize() if self.interactable else None,
                'partially_fogged': self.partially_fogged
            }
