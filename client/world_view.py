class WorldView(object):
    def __init__(self, my_avatar, map_centred_at_me, avatar_manager):
        self.my_avatar = my_avatar
        self.map_centred_at_me = map_centred_at_me
        self.avatar_manager = avatar_manager

    def get_my_avatar(self):
        return self.my_avatar

    def get_my_location(self):
        return self.get_my_avatar().location

    def get_my_health(self):
        return self.get_my_avatar().health

    def get_map_centred_at_me(self):
        return self.map_centred_at_me
