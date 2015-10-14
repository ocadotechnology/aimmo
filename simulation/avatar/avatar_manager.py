from simulation.avatar.avatar_wrapper import AvatarWrapper


class AvatarManager(object):
    def __init__(self, initial_avatars):
        self.avatarsById = {p.player_id: p for p in initial_avatars}

    def spawn(self, player_id, code, location):
        avatar = AvatarWrapper(location, code, player_id)
        self.avatarsById[player_id] = avatar
        return avatar

    @property
    def avatars(self):
        return self.avatarsById.viewvalues()
