import logging

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView

import os

from . import app_settings
from models import Avatar


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
def code(request):
    try:
        avatar = request.user.avatar_set.get(game_id=1)
    except Avatar.DoesNotExist:
        initial_code_file_name = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'avatar_examples/dumb_avatar.py',
        )
        with open(initial_code_file_name) as initial_code_file:
            initial_code = initial_code_file.read()
        avatar = Avatar.objects.create(owner=request.user, code=initial_code,
                                       game_id=1)
    if request.method == 'POST':
        avatar.code = request.POST['code']
        avatar.save()

        return _post_code_success_response("Your code was saved!")
    else:
        return HttpResponse(avatar.code)


def games(request):
    response = {
        'main': {
            'parameters': [],
            'users': [
                {
                    'id': avatar.owner_id,
                    'code': avatar.code,
                } for avatar in Avatar.objects.filter(game_id=1)
            ]
        }
    }
    return JsonResponse(response)


class WatchView(TemplateView):
    template_name = 'players/watch.html'

    def get_context_data(self, **kwargs):
        context = super(WatchView, self).get_context_data(**kwargs)
        context['game_url_base'], context['game_url_path'] = app_settings.GAME_SERVER_LOCATION_FUNCTION('main')
        context['current_user_player_key'] = self.request.user.pk
        return context
