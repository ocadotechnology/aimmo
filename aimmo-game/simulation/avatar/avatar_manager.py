from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.avatar.avatar_appearance import AvatarAppearance

import copy

class AvatarManager(object):
    """
    Stores all game avatars.
    """

    def __init__(self):
        self.avatars_by_id = {}

    def add_avatar(self, player_id, worker_url, location):
        avatar = AvatarWrapper(player_id, location, worker_url, AvatarAppearance("#000", "#ddd", "#777", "#fff"))
        self.avatars_by_id[player_id] = avatar
        return avatar

    def get_avatar(self, user_id):
        return self.avatars_by_id[user_id]

    def remove_avatar(self, user_id):
        if user_id in self.avatars_by_id:
            del self.avatars_by_id[user_id]

    @property
    def avatars(self):
        return self.avatars_by_id.viewvalues()

    # Note: I assume that this will be useful in the future. I have to figure out when
    # because right now it's just the same as 'avatars'. Otherwise:
    # TODO: Remove it.
    @property
    def active_avatars(self):
        return [player for player in self.avatars]
