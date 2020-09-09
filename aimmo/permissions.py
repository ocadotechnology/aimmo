from __future__ import absolute_import

from rest_framework import authentication, permissions

from common.permissions import CanDeleteGame


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


class CanUserPlay(permissions.BasePermission):
    """
    Used to verify that an incoming request is made by a user
    that's authorised to play an AIMMO game
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.can_user_play(request.user)


class CanDeleteGameOrReadOnly(permissions.BasePermission):
    """
    Used to verify that an incoming request is made by a user
    that's authorised to delete or view an AIMMO game
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == "PATCH":
            return GameHasToken().has_object_permission(request, view, obj)
        else:
            can_play = CanUserPlay().has_object_permission(request, view, obj)
            return CanDeleteGame().has_permission(request, view) and can_play
