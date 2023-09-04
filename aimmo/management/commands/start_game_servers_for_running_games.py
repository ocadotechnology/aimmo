from typing import Any, List

from django.core.management.base import BaseCommand

from aimmo.game_manager import GameManager
from aimmo.models import Game, GameSerializer


class Command(BaseCommand):
    help = """Start game servers for all games that have a status as running.
    To be used on redeploy when the fleet is deleted.
    """

    def handle(self, *args: Any, **options: Any):
        running_games: List[Game] = Game.objects.filter(status=Game.RUNNING)
        game_manager: GameManager = GameManager()

        for game in running_games:
            game_manager.create_game_server(game_id=game.id, game_data=GameSerializer(game).data)
