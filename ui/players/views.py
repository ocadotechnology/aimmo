import logging
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from models import Player
from simulation.avatar.avatar_wrapper import UserCodeException
from simulation.turn_manager import world_state_provider



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


def _post_code_error_response(message):
    return create_response("USER_ERROR", message)


def _post_server_error_response(message):
    return create_response("SERVER_ERROR", message)


def _post_code_success_response(message):
    return create_response("SUCCESS", message)


def create_response(status, message):
    response = {
        "status": status,
        "message": message
    }
    return HttpResponse(json.dumps(response))


@login_required
def code(request):
    if request.method == 'POST':
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
        
        return _post_code_success_response("Your code was saved!")
    else:
        return HttpResponse(request.user.player.code)
