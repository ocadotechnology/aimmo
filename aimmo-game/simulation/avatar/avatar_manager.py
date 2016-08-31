from simulation.event import DeathEvent
from simulation.game_settings import AVATAR_STARTING_HEALTH
from simulation.game_settings import SCORE_PENALTY_ON_DEATH

from .avatar_wrapper import AvatarWrapper
from .avatar_appearance import AvatarAppearance


class AvatarManager(object):
    """
    Stores all game avatars.
    """
    def __init__(self):
        self._avatars_by_id = {}

    def add_avatar(self, avatar_id, worker_url, location=None):
        avatar = AvatarWrapper(avatar_id, worker_url,
                               AvatarAppearance("#000", "#ddd", "#777", "#fff"))
        self._avatars_by_id[avatar_id] = avatar
        return avatar

    @staticmethod
    def spawn(world_map, avatar, location=None):
        avatar.location = (location if location is not None
                           else world_map.get_random_spawn_location())
        world_map.get_cell(avatar.location).avatar = avatar

    def get_avatar(self, avatar_id):
        return self._avatars_by_id[avatar_id]

    def remove_avatar(self, avatar_id):
        del self._avatars_by_id[avatar_id]

    @property
    def avatars(self):
        return self._avatars_by_id.viewvalues()

    @property
    def active_avatars(self):
        return [player for player in self.avatars]

    @property
    def num_avatars(self):
        return len(self.active_avatars)

    def process_deaths(self, world_map):
        for avatar in self.active_avatars:
            if avatar.health <= 0:
                self._kill_and_respawn(world_map, avatar)

    @staticmethod
    def _kill_and_respawn(world_map, avatar):
        avatar.health = AVATAR_STARTING_HEALTH
        avatar.score = max(0, avatar.score - SCORE_PENALTY_ON_DEATH)

        death_location = avatar.location

        world_map.get_cell(avatar.location).avatar = None
        avatar.location = world_map.get_random_spawn_location()
        world_map.get_cell(avatar.location).avatar = avatar

        avatar.add_event(DeathEvent(death_location, avatar.location))
