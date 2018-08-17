from simulation.location import Location


class AvatarState(object):
    def __init__(self, location, health, score):
        self.location = Location(**location)
        self.health = health
        self.score = score
