from functools import wraps

from rest_framework import authentication, permissions


def default_preview_user(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return wrapped


class HasToken(permissions.BasePermission):
    token_requested = False

    def has_object_permission(self, request, view, obj):
        print(self.token_requested)
        if request.method == "GET":
            passed_token_check = self.handle_get(request, obj)
        else:
            passed_token_check = self.handle_request(request, obj)

        return passed_token_check

    def handle_get(self, request, obj):
        if not self.token_requested:
            self.token_requested = True
            return True
        else:
            self.token_requested = True
            return self.check_for_token(request, obj)

    def handle_request(self, request, obj):
        return self.check_for_token(request, obj)

    def check_for_token(self, request, obj):
        try:
            return request.META["HTTP_TOKEN"] == obj.auth_token
        except KeyError:
            return False
        except AttributeError:
            return False
