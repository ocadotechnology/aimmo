from django.core.exceptions import PermissionDenied


class UserCannotPlayGameException(Exception):
    pass


class LimitExceeded(PermissionDenied):
    pass
