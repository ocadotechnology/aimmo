from __future__ import absolute_import

import logging
import os

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from . import forms
from . import game_renderer
from .app_settings import get_users_for_new_game
from .exceptions import UserCannotPlayGameException
from .models import Avatar, Game
from .game_creator import create_game, create_avatar_for_user
from .permissions import (
    CanDeleteGameOrReadOnly,
    CsrfExemptSessionAuthentication,
    GameHasToken,
)
from .serializers import GameSerializer

LOGGER = logging.getLogger(__name__)


def _post_code_success_response(message):
    return _create_response("SUCCESS", message)


def _create_response(status, message):
    response = {"status": status, "message": message}
    return JsonResponse(response)


@login_required
def code(request, id):
    if not request.user:
        return HttpResponseForbidden()
    game = get_object_or_404(Game, id=id)
    if not game.can_user_play(request.user):
        raise Http404
    try:
        avatar = game.avatar_set.get(owner=request.user)
    except Avatar.DoesNotExist:
        avatar = create_avatar_for_user(request.user, id)
    if request.method == "POST":
        avatar.code = request.POST["code"]
        avatar.save()
        return HttpResponse(status=200)
    else:
        return JsonResponse({"code": avatar.code})


class GameUsersView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (GameHasToken,)

    def get(self, request, id):
        game = get_object_or_404(Game, id=id)
        data = self.serialize_users(game)
        return JsonResponse(data)

    def serialize_users(self, game):
        users = {"main_avatar": None, "users": []}
        for avatar in game.avatar_set.all():
            if avatar.owner_id == game.main_user_id:
                users["main_avatar"] = avatar.id
            users["users"].append({"id": avatar.id, "code": avatar.code})
        return users


class GameViewSet(
    viewsets.GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    queryset = Game.objects.all()
    permission_classes = (CanDeleteGameOrReadOnly,)
    serializer_class = GameSerializer

    def list(self, request):
        response = {}
        for game in Game.objects.exclude_inactive():
            serializer = GameSerializer(game)
            response[game.pk] = serializer.data
        return Response(response)


def connection_parameters(request, game_id):
    """
    An API view which returns the correct connection settings required
    to run the game in different environments. These values will change
    depending on where the project is started (ie. local, etc).
    :param request: Django request object.
    :param game_id: Integer with the ID of the game.
    :return: JsonResponse object with the contents.
    """
    env_connection_settings = game_renderer.get_environment_connection_settings(game_id)

    avatar_id, response = get_avatar_id(request, game_id)

    if avatar_id:
        env_connection_settings.update({"avatar_id": avatar_id})
        return JsonResponse(env_connection_settings)
    else:
        return response


@csrf_exempt
@require_http_methods(["POST"])
def mark_game_complete(request, id):
    game = get_object_or_404(Game, id=id)
    game.completed = True
    game.static_data = request.body
    game.save()
    return HttpResponse("Done!")


class GameTokenView(APIView):
    """
    View to Game tokens, used to prove a request comes from a game.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (GameHasToken,)

    def get(self, request, id):
        """
        After the initial token request, we need to check where the
        request comes from. So for subsequent requests we verify that
        they came from the token-holder.
        """
        game = get_object_or_404(Game, id=id)
        self.check_object_permissions(self.request, game)
        return Response(data={"token": game.auth_token})

    def patch(self, request, id):
        game = get_object_or_404(Game, id=id)
        self.check_object_permissions(self.request, game)
        try:
            game.auth_token = request.data["token"]
            game.save()
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_403_FORBIDDEN)


@ensure_csrf_cookie
def watch_game(request, id):
    game = get_object_or_404(Game, id=id)
    if not game.can_user_play(request.user):
        raise Http404

    game.status = Game.RUNNING
    game.save()
    return game_renderer.render_game(request, game)


@login_required
def add_game(request):
    playable_games = request.user.playable_games.all()

    if request.method == "POST":
        form = forms.AddGameForm(playable_games, data=request.POST)
        if form.is_valid():
            users_to_add_to_game = get_users_for_new_game(request)
            game = create_game(request.user, form, users_to_add_to_game)
            return redirect("kurono/play", id=game.id)
    else:
        form = forms.AddGameForm(playable_games)
    return render(request, "players/add_game.html", {"form": form})


def current_avatar_in_game(request, game_id):
    avatar_id, response = get_avatar_id(request, game_id)

    if avatar_id:
        return JsonResponse({"current_avatar_id": avatar_id})
    else:
        return response


def get_avatar_id(request, game_id):
    avatar_id = None
    response = None

    try:
        avatar_id = game_renderer.get_avatar_id_from_user(
            user=request.user, game_id=game_id
        )
    except UserCannotPlayGameException:
        LOGGER.warning(
            "HTTP 401 returned. User {} unauthorised to play.".format(request.user.id)
        )
        response = HttpResponse("User unauthorized to play", status=401)
    except Avatar.DoesNotExist:
        LOGGER.warning(
            "Avatar does not exist for user {} in game {}".format(
                request.user.id, game_id
            )
        )
        response = HttpResponse("Avatar does not exist for this user", status=404)
    except Exception as e:
        LOGGER.error("Unknown error occurred while getting connection parameters!")
        LOGGER.error(e)
        response = HttpResponse(
            "Unknown error occurred when getting the current avatar", status=500
        )

    return avatar_id, response
