import os
import signal
import sys


def clean_tokens(*args):
    if os.environ.get("RUN_MAIN") == "true":
        from .models import Game

        games = Game.objects.all()
        for game in games:
            game.auth_token = ""
            game.save()

        print("stopped".upper())
    sys.exit(0)


signal.signal(signal.SIGINT, clean_tokens)
signal.signal(signal.SIGTERM, clean_tokens)
