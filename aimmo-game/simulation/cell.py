from abc import ABCMeta, abstractmethod

from simulation.action import MoveAction
from simulation.location import Location

class CellContent(object):
    __metaclass__ = ABCMeta

    def __init__(self, style):
        self.style = style

    @abstractmethod
    def is_habitable(self):
        pass

    @abstractmethod
    def generates_score(self):
        pass

    def get_style(self):
        return self.style

class Obstacle(CellContent):
    def __init__(self, *args, **kwargs):
        super(Obstacle, self).__init__(*args, **kwargs)

    def is_habitable(self):
        return False

    def generates_score(self):
        return False

class ScoreLocation(CellContent):
    def __init__(self, *args, **kwargs):
        super(ScoreLocation, self).__init__(*args, **kwargs)

    def is_habitable(self):
        return True

    def generates_score(self):
        return True

class Floor(CellContent):
    def __init__(self, *args, **kwargs):
        super(Floor, self).__init__(*args, **kwargs)

    def is_habitable(self):
        return True

    def generates_score(self):
        return False

class Cell(object):
    """
    Any position on the world grid.
    """

    def __init__(self, location, cell_content=Floor({}), partially_fogged=False):
        self.location = location
        self.cell_content = cell_content
        self.avatar = None
        self.pickup = None
        self.partially_fogged = partially_fogged
        self.actions = []

        # Used to update the map features in the current view of the user (score points on pickups).
        self.remove_from_scene = None
        self.add_to_scene = None

    def __repr__(self):
        return 'Cell({} h={} s={} a={} p={} f{})'.format(
            self.location, self.habitable, self.generates_score, self.avatar, self.pickup, self.partially_fogged)

    def __eq__(self, other):
        return self.location == other.location

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.location)

    @property
    def habitable(self):
        return self.cell_content.is_habitable()

    @property
    def generates_score(self):
        return self.cell_content.generates_score()

    @property
    def moves(self):
        return [move for move in self.actions if isinstance(move, MoveAction)]

    @property
    def is_occupied(self):
        return self.avatar is not None

    def serialise(self):
        if self.partially_fogged:
            return {
                'generates_score': self.generates_score,
                'location': self.location.serialise(),
                'partially_fogged': self.partially_fogged
            }
        else:
            return {
                'avatar': self.avatar.serialise() if self.avatar else None,
                'generates_score': self.generates_score,
                'habitable': self.habitable,
                'location': self.location.serialise(),
                'pickup': self.pickup.serialise() if self.pickup else None,
                'partially_fogged': self.partially_fogged
            }
