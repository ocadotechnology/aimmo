from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User)
    code = models.TextField()


# TODO: switch code back  to Avatar from Player to support players undoing their code changes
class Avatar(models.Model):
    player = models.ForeignKey(User)
