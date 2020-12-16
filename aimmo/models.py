from os import urandom

from base64 import urlsafe_b64encode
from common.models import Class
from django.contrib.auth.models import User
from django.db import models
from wagtail.snippets.models import register_snippet

from aimmo import app_settings

DEFAULT_WORKSHEET_ID = 1

GAME_GENERATORS = [("Main", "Open World")] + [  # Default
    ("Level%s" % i, "Level %s" % i) for i in range(1, app_settings.MAX_LEVEL + 1)
]


def generate_auth_token():
    return urlsafe_b64encode(urandom(16))


class WorksheetManager(models.Manager):
    def sorted(self):
        return self.get_queryset().order_by("sort_order")


@register_snippet
class Worksheet(models.Model):
    ERA_CHOICES = [
        (1, "future"),
        (2, "ancient"),
        (3, "modern day"),
        (4, "prehistoric"),
        (5, "broken future"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    image_path = models.CharField(max_length=255, blank=True)
    active_image_path = models.CharField(max_length=255, blank=True)
    era = models.PositiveSmallIntegerField(
        choices=ERA_CHOICES, default=ERA_CHOICES[0][0]
    )
    thumbnail_text = models.CharField(max_length=100, blank=True)
    thumbnail_image_path = models.CharField(max_length=255, blank=True)
    teacher_pdf_name = models.CharField(max_length=255, blank=True)
    student_pdf_name = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(default=0)

    objects = WorksheetManager()

    starter_code = models.TextField()

    def __str__(self):
        return f"{self.id}: {self.name}"


class Game(models.Model):
    RUNNING = "r"
    STOPPED = "s"
    PAUSED = "p"
    STATUS_CHOICES = ((RUNNING, "running"), (STOPPED, "stopped"), (PAUSED, "paused"))

    name = models.CharField(max_length=100, blank=True, null=True)
    auth_token = models.CharField(max_length=24, blank=True)
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
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="games_for_class",
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
    worksheet = models.ForeignKey(Worksheet, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("game_class", "worksheet")

    @property
    def is_active(self):
        return not self.completed

    def __str__(self):
        return self.name

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
