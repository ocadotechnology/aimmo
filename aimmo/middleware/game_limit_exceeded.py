from common.permissions import logged_in_as_teacher
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from aimmo.exceptions import GameLimitExceeded


class GameLimitExceededMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, GameLimitExceeded):
            if logged_in_as_teacher(request.user):
                messages.info(
                    request,
                    "The game is at full capacity. Please wait until someone returns from a "
                    "mission and frees up a vessel. Please try again later.",
                )
                return HttpResponseRedirect(reverse_lazy("teacher_aimmo_dashboard"))
            else:
                messages.info(
                    request,
                    "Oh no! It seems there are too many time travellers active already. "
                    "You'll need to wait until someone returns from a mission and frees up a ship. "
                    "Please try again later.",
                )
                return HttpResponseRedirect(reverse_lazy("student_aimmo_dashboard"))

        return None
