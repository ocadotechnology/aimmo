from functools import wraps

from rest_framework import authentication, permissions


def default_preview_user(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return wrapped


class HasToken(permissions.BasePermission):
    """
    Used to verify that an incoming request has permission
    to access a given object from the models.
    """

    token_requested = False

    def has_object_permission(self, request, view, obj):
        return self.check_for_token(request, obj)

    def handle_get(self, request, obj):
        if not self.token_requested:
            self.token_requested = True
            print(self.token_requested)
            return True
        else:
            return self.check_for_token(request, obj)

    def handle_request(self, request, obj):
        self.handle_get = self.handle_request
        return self.check_for_token(request, obj)

    def check_for_token(self, request, obj):
        try:
            return obj.auth_token == "" or request.META["HTTP_TOKEN"] == obj.auth_token
        except KeyError:
            return False
        except AttributeError:
            return False
