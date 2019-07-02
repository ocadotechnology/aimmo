import cPickle as pickle
import json
import logging
import os
from exceptions import UserCannotPlayGameException

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

import forms
import game_renderer
from app_settings import get_users_for_new_game, preview_user_required
from models import Avatar, Game, LevelAttempt
from permissions import (
    CanDeleteGameOrReadOnly,
    CsrfExemptSessionAuthentication,
    GameHasToken,
)
from serializers import GameSerializer

LOGGER = logging.getLogger(__name__)


def _post_code_success_response(message):
    return _create_response("SUCCESS", message)


def _create_response(status, message):
    response = {"status": status, "message": message}
    return JsonResponse(response)


@login_required
@preview_user_required
def code(request, id):
    if not request.user:
        return HttpResponseForbidden()
    game = get_object_or_404(Game, id=id)
    if not game.can_user_play(request.user):
        raise Http404
    try:
        avatar = game.avatar_set.get(owner=request.user)
    except Avatar.DoesNotExist:
        initial_code_file_name = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "avatar_examples/simple_avatar.py",
        )
        with open(initial_code_file_name) as initial_code_file:
            initial_code = initial_code_file.read()
        avatar = Avatar.objects.create(
            owner=request.user, code=initial_code, game_id=id
        )
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
        After the inital token request, we need to check where the
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


class ProgramView(TemplateView):
    template_name = "players/program.html"

    def get_context_data(self, **kwargs):
        context = super(ProgramView, self).get_context_data(**kwargs)
        game = get_object_or_404(Game, id=self.kwargs["id"])
        if not game.can_user_play(self.request.user):
            raise Http404
        context["game_id"] = int(self.kwargs["id"])
        return context


def watch_game(request, id):
    game = get_object_or_404(Game, id=id)
    if not game.can_user_play(request.user):
        raise Http404

    game.status = Game.RUNNING
    game.save()
    return game_renderer.render_game(request, game)


def watch_level(request, num):
    try:
        game = Game.objects.get(
            levelattempt__user=request.user, levelattempt__level_number=num
        )
    except Game.DoesNotExist:
        LOGGER.debug("Adding level")
        game = _add_and_return_level(num, request.user)
    LOGGER.debug("Displaying game with id %s", game.id)
    return game_renderer.render_game(request, game)


def _add_and_return_level(num, user):
    game = Game(
        generator="Level" + num, name="Level " + num, public=False, main_user=user
    )
    try:
        game.save()
    except ValidationError as e:
        LOGGER.warn(e)
        raise Http404
    game.can_play = [user]
    game.save()
    level_attempt = LevelAttempt(game=game, user=user, level_number=num)
    level_attempt.save()
    return game


@login_required
@preview_user_required
def add_game(request):
    playable_games = request.user.playable_games.all()

    if request.method == "POST":
        form = forms.AddGameForm(playable_games, data=request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.generator = "Main"
            game.owner = request.user
            game.main_user = request.user
            game.save()
            users = get_users_for_new_game(request)
            if users is not None:
                game.can_play.add(*users)
            return redirect("aimmo/play", id=game.id)
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


def csrfToken(request):
    if request.method == "GET":
        token = get_token(request)
        return JsonResponse({"csrfToken": token})
    else:
        return HttpResponse(status=405)
