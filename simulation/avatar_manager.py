from simulation.avatar import AvatarRunner, AvatarAppearance
from simulation.avatar import AvatarAppearance
from simulation.location import Location


class AvatarManager(object):
    def __init__(self, initial_avatars):
        self.avatarsById = {p.player_id: p for p in initial_avatars}

    def spawn(self, player_id, code, location):
        self.avatarsById[player_id] = AvatarRunner(location, code, player_id, AvatarAppearance("#000", "#ddd", "#777", "#fff"))

    @property
    def avatars(self):
        return self.avatarsById.viewvalues()

    def get_avatar_at(self, location):
        return next((a for a in self.avatars if a.location == location), None)
