from functools import wraps


def default_preview_user(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapped
