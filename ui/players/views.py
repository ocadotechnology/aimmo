from threading import Thread
import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import UserCreationForm

from simulation.avatar import UserCodeException
from simulation.avatar_manager import AvatarManager
from simulation.turn_manager import TurnManager
from simulation.turn_manager import world_state_provider
from simulation import world_map
from simulation.world_state import WorldState
from models import Player

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
            Player(user=user, code=INITIAL_CODE).save()
            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, authenticated_user)
            return redirect('program')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def run_game():
    print("Running game...")
    my_map = world_map.generate_map(15, 15, 0.1, 0.1)
    player_manager = AvatarManager([])
    world_state = WorldState(my_map, player_manager)
    turn_manager = TurnManager(world_state)

    turn_manager.run_game()


def start_game(request):
    thread = Thread(target=run_game)
    thread.start()
    return redirect('home')


def _post_code_error_response(message):
    return HttpResponse("USER_ERROR\n\n" + message)


def _post_server_error_response(message):
    return HttpResponse("SERVER_ERROR\n\n" + message)


def _post_code_ok_response():
    return HttpResponse("OK")


@login_required
def code(request):
    if request.method == 'POST':
        logger.info('POST ' + str(request.POST))
        request.user.player.code = request.POST['code']
        request.user.player.save()
        try:
            world = world_state_provider.lock_and_get_world()
            # TODO: deal with this in a better way
            if world is None:
                return _post_server_error_response('Your code was saved, but the game has not started yet!')

            world.player_changed_code(request.user.id, request.user.player.code)
        except UserCodeException as ex:
            return _post_code_error_response(ex.to_user_string())
        finally:
            world_state_provider.release_lock()
        
        return _post_code_ok_response()
    else:
        logger.info('GET ' + str(request.GET))
        return HttpResponse(request.user.player.code)
