from base64 import urlsafe_b64encode
from os import urandom

from django.contrib.auth.models import User
from django.db import models

from aimmo import app_settings

GAME_GENERATORS = [("Main", "Open World")] + [  # Default
    ("Level%s" % i, "Level %s" % i) for i in range(1, app_settings.MAX_LEVEL + 1)
]


def generate_auth_token():
    return urlsafe_b64encode(urandom(16))


class GameQuerySet(models.QuerySet):
    def for_user(self, user):
        if user.is_authenticated():
            return self.filter(models.Q(public=True) | models.Q(can_play=user))
        else:
            return self.filter(public=True)

    def exclude_inactive(self):
        return self.filter(completed=False)


class Game(models.Model):
    RUNNING = "r"
    STOPPED = "s"
    PAUSED = "p"
    STATUS_CHOICES = ((RUNNING, "running"), (STOPPED, "stopped"), (PAUSED, "paused"))

    name = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=24, blank=True)
    owner = models.ForeignKey(User, blank=True, null=True, related_name="owned_games")
    public = models.BooleanField(default=False)
    can_play = models.ManyToManyField(
        User,
        related_name="playable_games",
        help_text="List of auth_user IDs of users who are allowed to play and have access to the game.",
    )
    completed = models.BooleanField(default=False)
    main_user = models.ForeignKey(
        User, blank=True, null=True, related_name="games_for_user"
    )
    objects = GameQuerySet.as_manager()
    static_data = models.TextField(blank=True, null=True)

    # Game config
    generator = models.CharField(
        max_length=20, choices=GAME_GENERATORS, default=GAME_GENERATORS[0][0]
    )
    target_num_cells_per_avatar = models.FloatField(default=16)
    target_num_score_locations_per_avatar = models.FloatField(default=0.5)
    score_despawn_chance = models.FloatField(default=0.05)
    target_num_pickups_per_avatar = models.FloatField(default=1.2)
    pickup_spawn_chance = models.FloatField(default=0.1)
    obstacle_ratio = models.FloatField(default=0.1)
    start_height = models.IntegerField(default=31)
    start_width = models.IntegerField(default=31)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=RUNNING)

    @property
    def is_active(self):
        return not self.completed

    def __str__(self):
        return self.name

    def can_user_play(self, user):
        return self.public or user in self.can_play.all()

    def settings_as_dict(self):
        return {
            "GENERATOR": self.generator,
            "OBSTACLE_RATIO": self.obstacle_ratio,
            "PICKUP_SPAWN_CHANCE": self.pickup_spawn_chance,
            "SCORE_DESPAWN_CHANCE": self.score_despawn_chance,
            "START_HEIGHT": self.start_height,
            "START_WIDTH": self.start_width,
            "TARGET_NUM_CELLS_PER_AVATAR": self.target_num_cells_per_avatar,
            "TARGET_NUM_PICKUPS_PER_AVATAR": self.target_num_pickups_per_avatar,
            "TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR": self.target_num_score_locations_per_avatar,
        }

    def save(self, *args, **kwargs):
        super(Game, self).full_clean()
        super(Game, self).save(*args, **kwargs)


class Avatar(models.Model):
    owner = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    code = models.TextField()
    auth_token = models.CharField(max_length=24, default=generate_auth_token)

    class Meta:
        unique_together = ("owner", "game")


class LevelAttempt(models.Model):
    level_number = models.IntegerField()
    user = models.ForeignKey(User)
    game = models.OneToOneField(Game)

    class Meta:
        unique_together = ("level_number", "user")
