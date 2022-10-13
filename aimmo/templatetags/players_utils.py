from aimmo.models import Game
from django import template

from common.permissions import logged_in_as_teacher

register = template.Library()


def get_user_playable_games(context, base_url):
    # Only called by teacher to create games table
    user = context.request.user
    teacher = user.new_teacher
    if logged_in_as_teacher(user):
        playable_games = list(Game.objects.filter(owner=user, is_archived=False))
        if teacher.is_admin:
            playable_games += list(
                Game.objects.filter(game_class__teacher__school=teacher.school, is_archived=False).exclude(owner=user)
            )
    else:
        playable_games = Game.objects.none()
    return {
        "user": user,
        "base_url": base_url,
        "open_play_games": playable_games if user.is_authenticated else None,
    }
