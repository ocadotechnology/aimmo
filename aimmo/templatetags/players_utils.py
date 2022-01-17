from aimmo.models import Game
from django import template

from common.permissions import logged_in_as_student, logged_in_as_teacher

register = template.Library()


def get_user_playable_games(context, base_url):
    # Only called by teacher to create games table
    user = context.request.user
    if logged_in_as_teacher(user):
        playable_games = Game.objects.filter(
            game_class__teacher=user.userprofile.teacher, is_archived=False
        )
    else:
        playable_games = Game.objects.none()
    return {
        "base_url": base_url,
        "open_play_games": playable_games if user.is_authenticated else None,
    }
