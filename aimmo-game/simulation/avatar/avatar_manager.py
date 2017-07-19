from avatar_wrapper import AvatarWrapper
from avatar_appearance import AvatarAppearance

class AvatarManager(object):
    """
    Stores all game avatars. An avatar can belong to on of the following three lists:
    - avatars_by_id: If the avatar is on the game.
    - created_avatars_by_id: If the avatar has ust been created. The avatar is put in
      this list at first then when the client know about it it's but to avatars_by_id.
    - deleted_avatars_by_id: Before completely removing the avatar from the list, the
      avatar is put in this list and then, when the client knows that it has to delete
      it from the scene, it's removed completely.
    """

    def __init__(self):
        self.avatars_by_id = {}
        self.avatars_to_create_by_id = {}
        self.avatars_to_delete_by_id = {}

    def add_avatar(self, player_id, worker_url, location):
        avatar = AvatarWrapper(player_id, location, worker_url, AvatarAppearance("#000", "#ddd", "#777", "#fff"))
        self.avatars_to_create_by_id[player_id] = avatar
        return avatar

    def get_avatar(self, user_id):
        return self.avatars_by_id[user_id]

    def remove_avatar(self, user_id):
        if user_id in self.avatars_by_id:
            self.avatars_to_delete_by_id[user_id] = self.avatars_by_id[user_id][:]
            del self.avatars_by_id[user_id]

    @property
    def avatars(self):
        return self.avatars_by_id.viewvalues()

    @property
    def avatars_to_create(self):
        return self.avatars_to_create_by_id.viewvalues()

    @property
    def avatars_to_delete(self):
        return self.avatars_to_delete_by_id.viewvalues()

    # Returns the newly created avatars and then puts them in the normal avatars list.
    @property
    def created_avatars(self):
        created_avatars_array = self.avatars_to_create_by_id.viewvalues()[:]
        self.avatars_by_id.update(dict(self.avatars_to_create_by_id))
        self.avatars_to_create_by_id.clear()

        return created_avatars_array

    # Returns the avatars that need to be removed from the scene.
    @property
    def deleted_avatars(self):
        deleted_avatars_array = self.avatars_to_delete_by_id.viewvalues()[:]
        self.avatars_to_create_by_id.clear()

        return deleted_avatars_array

    # Note: I assume that this will be useful in the future. I have to figure out when
    # because right now it's just the same as 'avatars'. Otherwise:
    # TODO: Remove it.
    @property
    def active_avatars(self):
        return [player for player in self.avatars]
