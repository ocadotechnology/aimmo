from base64 import urlsafe_b64encode
from django.contrib.auth.models import User
from django.db import models
from os import urandom


def generate_auth_token():
    return urlsafe_b64encode(urandom(16))


class Game(models.Model):
    name = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=24, default=generate_auth_token)
    owner = models.ForeignKey(User, null=True, related_name='owned_games')
    public = models.BooleanField(default=True)
    can_play = models.ManyToManyField(User, related_name='playable_games')

    # Game config
    target_num_cells_per_avatar = models.FloatField(default=16)
    target_num_score_locations_per_avatar = models.FloatField(default=0.5)
    score_despawn_chance = models.FloatField(default=0.02)
    target_num_pickups_per_avatar = models.FloatField(default=0.5)
    pickup_spawn_chance = models.FloatField(default=0.02)
    obstacle_ratio = models.FloatField(default=0.1)
    start_height = models.IntegerField(default=11)
    start_width = models.IntegerField(default=11)

    def can_user_play(self, user):
        return self.public or user in self.can_play.all()

    def settings_as_dict(self):
        return {
            'TARGET_NUM_CELLS_PER_AVATAR': self.target_num_cells_per_avatar,
            'TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR': self.target_num_score_locations_per_avatar,
            'SCORE_DESPAWN_CHANCE': self.score_despawn_chance,
            'TARGET_NUM_PICKUPS_PER_AVATAR': self.target_num_pickups_per_avatar,
            'PICKUP_SPAWN_CHANCE': self.pickup_spawn_chance,
            'OBSTACLE_RATIO': self.obstacle_ratio,
            'START_HEIGHT': self.start_height,
            'START_WIDTH': self.start_width,
        }


class Avatar(models.Model):
    owner = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    code = models.TextField()
    auth_token = models.CharField(max_length=24, default=generate_auth_token)

    class Meta:
        unique_together = ('owner', 'game')
