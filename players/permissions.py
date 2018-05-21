from functools import wraps
from django.http import HttpResponse

def preview_user(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        u = request.user
        if (not hasattr(u, 'userprofile') or not hasattr(u.userprofile, 'preview_user') or not u.userprofile.preview_user):
            return HttpResponse('Unauthorized', status=401)

        return view_func(request, *args, **kwargs)

    return wrapped
