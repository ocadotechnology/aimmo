from django.apps import AppConfig


class AimmoConfig(AppConfig):
    name = "aimmo"

    def ready(self):
        games = self.get_model("Game").objects.all()
        for game in games:
            game.auth_token = ""
            game.save()
