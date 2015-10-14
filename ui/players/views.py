from threading import Thread
import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from simulation.avatar.avatar_wrapper import UserCodeException
from simulation.avatar.avatar_manager import AvatarManager
import simulation.map_generator
from simulation.turn_manager import TurnManager
from simulation.turn_manager import world_state_provider
from simulation.game_state import GameState
from models import Player

import json

GAME_NOT_STARTED = "GAME_NOT_STARTED"
OK = "OK"
USER_ERROR = "USER_ERROR"

INITIAL_CODE = '''from simulation.action import MoveAction
from simulation import direction


class Avatar(object):
    def handle_turn(self, world_state, events):
        import random
        directions = (direction.EAST, direction.SOUTH, direction.WEST, direction.NORTH)
        return MoveAction(random.choice(directions))
'''

# TODO: move all views that just render a template over to using django generic views

logger = logging.getLogger("views")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            with open("simulation/avatar_examples/dumb_avatar.py") as initial_code_file:
                initial_code = initial_code_file.read()

            Player(user=user, code=initial_code).save()
            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, authenticated_user)
            return redirect('program')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def run_game():
    print("Running game...")
    my_map = simulation.map_generator.generate_map(15, 15, 0.1)
    player_manager = AvatarManager([])
    game_state = GameState(my_map, player_manager)
    turn_manager = TurnManager(game_state)

    turn_manager.run_game()


def start_game(request):
    thread = Thread(target=run_game)
    thread.start()
    return redirect('home')


def _post_code_error_response(message):
    return HttpResponse(json.dumps({"status": USER_ERROR, "message": message}))

def _post_server_error_response(typ):
    return HttpResponse(json.dumps({"status": typ}))


def _post_code_ok_response():
    return HttpResponse(json.dumps({"status": OK }))


@login_required
def code(request):
    if request.method == 'POST':
        request.user.player.code = request.POST['code']
        request.user.player.save()
        try:
            world = world_state_provider.lock_and_get_world()
            # TODO: deal with this in a better way
            if world is None:
                return _post_server_error_response(GAME_NOT_STARTED)

            world.player_changed_code(request.user.id, request.user.player.code)
        except UserCodeException as ex:
            return _post_code_error_response(ex.to_user_string())
        finally:
            world_state_provider.release_lock()
        
        return _post_code_ok_response()
    else:
        return HttpResponse(request.user.player.code)
