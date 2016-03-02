from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.avatar.avatar_appearance import AvatarAppearance


class AvatarManager(object):
    """
    Stores all game avatars.
    """

    def __init__(self, initial_avatars):
        self.avatarsById = {p.player_id: p for p in initial_avatars}

    def spawn(self, player_id, code, location):
        avatar = AvatarWrapper(location, code, player_id, AvatarAppearance("#000", "#ddd", "#777", "#fff"))
        self.avatarsById[player_id] = avatar
        return avatar

    @property
    def avatars(self):
        return self.avatarsById.viewvalues()

    @property
    def active_avatars(self):
        return [player for player in self.avatars if player.code]
