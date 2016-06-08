import logging

from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from models import Player


# TODO: move all views that just render a template over to using django generic views

logger = logging.getLogger("views")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, authenticated_user)
            return redirect('program')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def _post_code_success_response(message):
    return create_response("SUCCESS", message)


def create_response(status, message):
    response = {
        "status": status,
        "message": message
    }
    return JsonResponse(response)


@login_required
def code(request):
    try:
        player = request.user.player
    except Player.DoesNotExist:
        with open("players/avatar_examples/dumb_avatar.py") as initial_code_file:
            initial_code = initial_code_file.read()
        player = Player.objects.create(user=request.user, code=initial_code)
    if request.method == 'POST':
        player.code = request.POST['code']
        player.save()

        return _post_code_success_response("Your code was saved!")
    else:
        return HttpResponse(player.code)


def games(request):
    response = {
        'main': {
            'parameters': [],
            'users': [
                {
                    'id': player.user.pk,
                    'code': player.code,
                } for player in Player.objects.all()
            ]
        }
    }
    return JsonResponse(response)
