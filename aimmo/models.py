import secrets
import typing as t

from common.models import Class
from common.models import Teacher
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from aimmo import app_settings
from aimmo.exceptions import GameLimitExceeded
from aimmo.game_manager import GameManager
from aimmo.worksheets import WORKSHEETS

DEFAULT_WORKSHEET_ID = 1

GAME_GENERATORS = [("Main", "Open World")] + [  # Default
    ("Level%s" % i, "Level %s" % i) for i in range(1, app_settings.MAX_LEVEL + 1)
]

MAX_GAMES_LIMIT = 15


def generate_game_auth_token():
    return secrets.token_urlsafe(nbytes=32)[:48]


def generate_avatar_auth_token():
    return secrets.token_urlsafe(nbytes=16)[:24]


class GameQuerySet(models.QuerySet):
    """
    Manager from the Game model to ensure the max game limit cannot be exceeded when calling update()
    """

    def update(self, **kwargs) -> int:
        running_games = Game.objects.filter(status=Game.RUNNING)

        if kwargs.get("status") == Game.RUNNING and running_games.union(self).count() > MAX_GAMES_LIMIT:
            raise GameLimitExceeded
        return super().update(**kwargs)


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
        blank=True,
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
    created_by = models.ForeignKey(
        Teacher,
        blank=True,
        null=True,
        related_name="game_created_by_teacher",
        on_delete=models.SET_NULL,
    )

    # Game config
    generator = models.CharField(max_length=20, choices=GAME_GENERATORS, default=GAME_GENERATORS[0][0])
    target_num_cells_per_avatar = models.FloatField(default=16)
    target_num_score_locations_per_avatar = models.FloatField(default=0.5)
    score_despawn_chance = models.FloatField(default=0.05)
    # Set default pickup num to 0 to remove artefacts from worksheet 1
    target_num_pickups_per_avatar = models.FloatField(default=0)
    pickup_spawn_chance = models.FloatField(default=0.1)
    obstacle_ratio = models.FloatField(default=0.1)
    start_height = models.IntegerField(default=31)
    start_width = models.IntegerField(default=31)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=RUNNING)
    worksheet_id = models.IntegerField(default=DEFAULT_WORKSHEET_ID)
    is_archived = models.BooleanField(default=False)
    creation_time = models.DateTimeField(default=timezone.now, null=True)

    objects: GameQuerySet = GameQuerySet.as_manager()

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
        is_student_in_class = self.game_class.students.filter(new_user=user).exists()
        is_teacher_class_owner = user == self.game_class.teacher.new_user
        is_teacher_admin = (
            hasattr(user.userprofile, "teacher")
            and user.userprofile.teacher.school == self.game_class.teacher.school
            and user.userprofile.teacher.is_admin
        )
        try:
            return is_student_in_class or is_teacher_class_owner or is_teacher_admin
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

    def save(self, **kwargs):
        if self.id is None:
            self.owner = self.game_class.teacher.new_user
            self.main_user = self.game_class.teacher.new_user

            if self.created_by is None:
                self.created_by = self.main_user.userprofile.teacher

            super(Game, self).save(**kwargs)

            if not Avatar.objects.filter(owner=self.created_by.new_user, game=self).exists():
                Avatar.objects.create(game=self, owner=self.created_by.new_user)

            game_manager = GameManager()
            game_manager.create_game_secret(game_id=self.id, token=self.auth_token)
        else:
            super(Game, self).save(**kwargs)


@receiver(models.signals.pre_save, sender=Game)
def check_game_limit(sender: t.Type[Game], instance: Game, **kwargs):
    if instance.status == Game.RUNNING and sender.objects.filter(status=Game.RUNNING).count() >= MAX_GAMES_LIMIT:
        raise GameLimitExceeded


class Avatar(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    code = models.TextField()
    auth_token = models.CharField(max_length=24, blank=True, default=generate_avatar_auth_token)

    def save(self, **kwargs):
        if self.id is None and self.code == "":
            self.code = self.game.worksheet.starter_code

        super(Avatar, self).save(**kwargs)

    class Meta:
        unique_together = ("owner", "game")
