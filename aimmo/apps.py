from django.apps import AppConfig


class AimmoConfig(AppConfig):
    name = "aimmo"

    def ready(self):
        Game = self.get_model("Game")

        games = Game.objects.all()
        for game in games:
            game.auth_token = ""
            game.save()
