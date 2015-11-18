from threading import Thread

from django.contrib.auth.models import User
from django.db import models

from simulation import map_generator
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_state import GameState
from simulation.turn_manager import TurnManager


class Player(models.Model):
    user = models.OneToOneField(User)
    code = models.TextField()


# TODO: switch code back  to Avatar from Player to support players undoing their code changes
class Avatar(models.Model):
    player = models.ForeignKey(User)


# TODO: this is temporary until we split the UI from the back-end
def run_game():
    print("Running game...")
    my_map = map_generator.generate_map(15, 15, 0.1)
    player_manager = AvatarManager([])
    game_state = GameState(my_map, player_manager)
    turn_manager = TurnManager(game_state)

    turn_manager.run_game()

thread = Thread(target=run_game)
thread.start()
