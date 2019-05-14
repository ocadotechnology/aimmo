from functools import wraps

from rest_framework import authentication, permissions


def default_preview_user(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return wrapped


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return False


class GameHasToken(permissions.BasePermission):
    """
    Used to verify that an incoming request has permission
    to access a given object from the models.

    This is done on a per object basis. The object must have an `auth_token`
    attribute to be used with this permission class.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return self.check_for_token(request, obj)

    def check_for_token(self, request, obj):
        try:
            return (
                obj.auth_token == ""
                or request.META["HTTP_GAME_TOKEN"] == obj.auth_token
            )
        except (KeyError, AttributeError):
            return False
