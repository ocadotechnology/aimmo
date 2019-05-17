from django.apps import AppConfig


class AimmoConfig(AppConfig):
    name = "aimmo"

    def ready(self):
        games = self.get_model("Game").objects.all()
        print("########################################")
        print(games)
        print("########################################")
        for game in games:
            game.auth_token = ""
            game.save()
