from django.contrib.auth.models import User
from django.db import models


class Player(models.Model):
    user = models.OneToOneField(User)
    code = models.TextField()
