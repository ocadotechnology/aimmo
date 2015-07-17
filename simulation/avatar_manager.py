from simulation.avatar import AvatarRunner
from simulation.location import Location

class AvatarManager(object):
    def __init__(self, initial_avatars):
        self.avatarsById = {p.id: p for p in initial_avatars}

    def player_changed_code(self, playerId, code):
        avatar = self.avatarsById.get(playerId)
        if not avatar:
            avatar = AvatarRunner(Location(0, 0), code, playerId)
            self.avatarsById[playerId] = avatar
        avatar.set_code(code)

