from simulation.avatar.avatar_manager import AvatarManager
from simulation.avatar.avatar_wrapper import AvatarWrapper


class MockAvatarManager(AvatarManager):
    def add_avatar(self, player_id, location=None):
        avatar = AvatarWrapper(player_id, None, None)
        self.avatars_by_id[player_id] = avatar
        return avatar
