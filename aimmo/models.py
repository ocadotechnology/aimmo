from os import urandom

from base64 import urlsafe_b64encode
from common.models import Class
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from aimmo import app_settings
from aimmo.worksheets import WORKSHEETS

DEFAULT_WORKSHEET_ID = 1

GAME_GENERATORS = [("Main", "Open World")] + [  # Default
    ("Level%s" % i, "Level %s" % i) for i in range(1, app_settings.MAX_LEVEL + 1)
]


def generate_auth_token():
    return urlsafe_b64encode(urandom(16))


class Game(models.Model):
    RUNNING = "r"
    STOPPED = "s"
    PAUSED = "p"
    STATUS_CHOICES = ((RUNNING, "running"), (STOPPED, "stopped"), (PAUSED, "paused"))

    name = models.CharField(max_length=100, blank=True, null=True)
    auth_token = models.CharField(max_length=48, blank=True)
    owner = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="owned_games",
        on_delete=models.SET_NULL,
    )
    game_class = models.ForeignKey(
        Class,
        verbose_name="Class",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    public = models.BooleanField(default=False)
    can_play = models.ManyToManyField(
        User,
        related_name="playable_games",
        help_text="List of auth_user IDs of users who are allowed to play and have access to the game.",
    )
    completed = models.BooleanField(default=False)
    main_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="games_for_user",
        on_delete=models.SET_NULL,
    )
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
    worksheet_id = models.IntegerField(default=DEFAULT_WORKSHEET_ID)
    is_archived = models.BooleanField(default=False)
    creation_time = models.DateTimeField(default=timezone.now, null=True)

    @property
    def is_active(self):
        return not self.completed

    @property
    def worksheet(self):
        return WORKSHEETS.get(self.worksheet_id)

    def __str__(self):
        return str(self.id)

    def can_user_play(self, user: User) -> bool:
        """Checks whether the given user has permission to play the game.

        A user can play the game if they are part of the game's class or
        the teacher of that class.

        Args:
            user: A standard django User object

        Returns:
            bool: True if user can play the game, False otherwise
        """
        try:
            return (
                self.game_class.students.filter(new_user=user).exists()
                or user == self.game_class.teacher.new_user
            )
        except AttributeError:
            return False

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    code = models.TextField()
    auth_token = models.CharField(max_length=24, default=generate_auth_token)

    class Meta:
        unique_together = ("owner", "game")
