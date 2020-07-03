from typing import List
from simulation.avatar.avatar_wrapper import AvatarWrapper
from simulation.avatar.avatar_appearance import AvatarAppearance
from simulation.worksheet import WORKSHEET, WorksheetData


class AvatarManager(object):
    """
    Stores all game avatars.
    """

    def __init__(self, worksheet: WorksheetData = WORKSHEET):
        self.avatars_by_id = {}
        self.worksheet = worksheet

    def add_avatar(self, player_id, location):
        avatar = AvatarWrapper(
            player_id, location, AvatarAppearance("#000", "#ddd", "#777", "#fff")
        )
        self.avatars_by_id[player_id] = avatar
        return avatar

    def get_avatar(self, user_id):
        return self.avatars_by_id[user_id]

    def remove_avatar(self, user_id):
        del self.avatars_by_id[user_id]

    def clear_all_avatar_logs(self):
        for avatar in self.avatars:
            avatar.clear_logs()

    @property
    def avatars(self) -> List[AvatarWrapper]:
        return list(self.avatars_by_id.values())

    @property
    def active_avatars(self):
        return self.avatars[:]

    def serialize_players(self):
        """
        To be called on a required update of players in the front-end of the game.
        """

        return [
            self.worksheet.avatar_state_serializer(avatar) for avatar in self.avatars
        ]
