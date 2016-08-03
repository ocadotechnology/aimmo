import logging

import cPickle as pickle
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView

import os

from . import app_settings
from models import Avatar, Game


LOGGER = logging.getLogger(__name__)


def _post_code_success_response(message):
    return _create_response("SUCCESS", message)


def _create_response(status, message):
    response = {
        "status": status,
        "message": message
    }
    return JsonResponse(response)


@login_required
def code(request, id):
    game = get_object_or_404(Game, id=id)
    if not game.can_user_play(request.user):
        raise Http404
    try:
        avatar = game.avatar_set.get(owner=request.user)
    except Avatar.DoesNotExist:
        initial_code_file_name = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'avatar_examples/dumb_avatar.py',
        )
        with open(initial_code_file_name) as initial_code_file:
            initial_code = initial_code_file.read()
        avatar = Avatar.objects.create(owner=request.user, code=initial_code,
                                       game_id=id)
    if request.method == 'POST':
        avatar.code = request.POST['code']
        avatar.save()
        return _post_code_success_response("Your code was saved!")
    else:
        return HttpResponse(avatar.code)


def list_games(request):
    response = {
        game.pk:
            {
                'name': game.name,
                'settings': pickle.dumps(game.settings_as_dict()),
            } for game in Game.objects.all()
    }
    return JsonResponse(response)


def get_game(request, id):
    game = get_object_or_404(Game, id=id)
    response = {
        'main': {
            'parameters': [],
            'users': [
                {
                    'id': avatar.owner_id,
                    'code': avatar.code,
                } for avatar in game.avatar_set.all()
            ]
        }
    }
    return JsonResponse(response)


class ProgramView(TemplateView):
    template_name = 'players/program.html'

    def get_context_data(self, **kwargs):
        context = super(ProgramView, self).get_context_data(**kwargs)
        context['games'] = Game.objects.all()
        return context


def get_games_for_user(user):
    return Game.objects.filter(Q(public=True) | Q(can_play=user))


def watch_game(request, id):
    game = get_object_or_404(Game, id=id)
    if not game.can_user_play(request.user):
        raise Http404
    context = {
        'current_user_player_key': request.user.pk,
        'games': get_games_for_user(request.user),
        'active_game': int(id),
    }
    context['game_url_base'], context['game_url_path'] = app_settings.GAME_SERVER_LOCATION_FUNCTION(id)
    return render(request, 'players/watch.html', context)


def add_game(request):
    name = "Game %d" % (Game.objects.count() + 1)
    game = Game(name=name)
    game.save()
    return redirect('aimmo/program')


class WatchList(ListView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super(WatchList, self).get_context_data(**kwargs)
        context['games'] = get_games_for_user(self.request.user)
        return context
