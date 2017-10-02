from simulation.geography.location import Location


class AvatarState(object):

    def __init__(self, location, health, score, events):
        self.location = Location(**location)
        self.health = health
        self.score = score
        self.events = events
