from django.apps import AppConfig


class AimmoConfig(AppConfig):
    name = "aimmo"

    def ready(self):
        from .models import Game

        games = Game.objects.all()
        for game in games:
            game.auth_token = ""
            game.save()
