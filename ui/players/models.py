from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User)


class Avatar(models.Model):
    player = models.ForeignKey(User)
    code = models.TextField()