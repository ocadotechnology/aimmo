from functools import wraps

from django.conf import settings
from django.utils.module_loading import import_string
from django.contrib.auth.models import User
from rest_framework import permissions

#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_URL_FUNCTION = getattr(settings, "AIMMO_GAME_SERVER_URL_FUNCTION", None)
GAME_SERVER_PORT_FUNCTION = getattr(settings, "AIMMO_GAME_SERVER_PORT_FUNCTION", None)
GAME_SERVER_SSL_FLAG = getattr(settings, "AIMMO_GAME_SERVER_SSL_FLAG", False)
PREVIEW_USER_AIMMO_DECORATOR = getattr(settings, "PREVIEW_USER_AIMMO_DECORATOR", None)
CAN_DELETE_GAME_CLASS = getattr(settings, "CAN_DELETE_GAME_CLASS", None)
USERS_FOR_NEW_AIMMO_GAME = getattr(settings, "USERS_FOR_NEW_AIMMO_GAME", None)


def default_preview_user(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return wrapped


class DummyPermission(permissions.BasePermission):
    """
    Used to mock general permissions
    """

    def has_permission(self, request, view):
        return True


def get_aimmo_preview_user_decorator():
    """
    This function is used to import a decorator from portal, which
    checks whether the logged in user is a preview user.

    :return: A function decorator
    """
    if PREVIEW_USER_AIMMO_DECORATOR:
        func = import_string(PREVIEW_USER_AIMMO_DECORATOR)
        return func
    return default_preview_user


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


preview_user_required = get_aimmo_preview_user_decorator()
CanDelete = get_can_delete_game_class()

MAX_LEVEL = 1
