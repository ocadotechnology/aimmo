from simulation.location import Location


class AvatarState(object):
    def __init__(self, location, health, score, backpack, id, orientation):
        self.location = Location(**location)
        self.health = health
        self.score = score
        self.backpack = backpack
        self.id = id
        self.orientation = orientation
