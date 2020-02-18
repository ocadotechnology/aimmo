from simulation.location import Location


class AvatarState(object):
    def __init__(self, location, health, score, number_of_artefacts):
        self.location = Location(**location)
        self.health = health
        self.score = score
        self.number_of_artefacts = number_of_artefacts
