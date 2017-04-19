from base64 import urlsafe_b64encode
from django.contrib.auth.models import User
from django.db import models
from os import urandom


def generate_auth_token():
    return urlsafe_b64encode(urandom(16))


class Game(models.Model):
    name = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=24, default=generate_auth_token)


class Avatar(models.Model):
    owner = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    code = models.TextField()
    auth_token = models.CharField(max_length=24, default=generate_auth_token)

    class Meta:
        unique_together = ('owner', 'game')
