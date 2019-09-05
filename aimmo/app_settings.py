from functools import wraps

from django.conf import settings
from django.utils.module_loading import import_string
from django.contrib.auth.models import User
from rest_framework import permissions

#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_URL_FUNCTION = getattr(settings, "AIMMO_GAME_SERVER_URL_FUNCTION", None)
GAME_SERVER_PORT_FUNCTION = getattr(settings, "AIMMO_GAME_SERVER_PORT_FUNCTION", None)
GAME_SERVER_SSL_FLAG = getattr(settings, "AIMMO_GAME_SERVER_SSL_FLAG", False)
CAN_DELETE_GAME_CLASS = getattr(settings, "CAN_DELETE_GAME_CLASS", None)
USERS_FOR_NEW_AIMMO_GAME = getattr(settings, "USERS_FOR_NEW_AIMMO_GAME", None)


class DummyPermission(permissions.BasePermission):
    """
    Used to mock general permissions
    """

    def has_permission(self, request, view):
        return True


def get_users_for_new_game(request):
    """
    Imports and calls a function defined in portal, that decides
    which users should be added to the newly created game.
    :param request:
    :return: List of User objects
    """
    if USERS_FOR_NEW_AIMMO_GAME:
        func = import_string(USERS_FOR_NEW_AIMMO_GAME)
        return func(request)
    return User.objects.all()


def get_can_delete_game_class():
    if CAN_DELETE_GAME_CLASS:
        return import_string(CAN_DELETE_GAME_CLASS)
    return DummyPermission


CanDelete = get_can_delete_game_class()

MAX_LEVEL = 1
