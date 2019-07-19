from django.apps import AppConfig
from django.db.models.signals import post_migrate


def clear_tokens(sender, **kwargs):
    game_model = sender.get_model("Game")
    games = game_model.objects.all()
    games.update(auth_token="")


class AimmoAppConfig(AppConfig):
    name = "aimmo"

    def ready(self):
        post_migrate.connect(clear_tokens, sender=self)
