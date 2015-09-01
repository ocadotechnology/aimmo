from simulation.avatar import AvatarRunner, AvatarAppearance
from simulation.avatar import AvatarAppearance
from simulation.location import Location


class AvatarManager(object):
    def __init__(self, initial_avatars):
        self.avatarsById = {p.player_id: p for p in initial_avatars}

    def spawn(self, player_id, code, location):
        avatar = AvatarRunner(location, code, player_id, AvatarAppearance("#000", "#ddd", "#777", "#fff"))
        self.avatarsById[player_id] = avatar
        return avatar

    @property
    def avatars(self):
        return self.avatarsById.viewvalues()
