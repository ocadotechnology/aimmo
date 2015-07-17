class AvatarManager(object):
    def __init__(self, initial_avatars):
        self.avatarsById = {p.player_id: p for p in initial_avatars}

    def player_changed_code(self, player_id, code):
        avatar = self.avatarsById[player_id]
        avatar.set_code(code)

    @property
    def avatars(self):
        return self.avatarsById.viewvalues()