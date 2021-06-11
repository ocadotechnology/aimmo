from aimmo.models import Game
from django import template

from common.permissions import logged_in_as_student, logged_in_as_teacher

register = template.Library()


@register.inclusion_tag("players/dropdown.html", takes_context=True)
def game_dropdown_list(context, base_url):
    return get_user_playable_games(context, base_url)


def get_user_playable_games(context, base_url):
    user = context.request.user
    if logged_in_as_student(user):
        playable_games = user.userprofile.student.class_field.game
    elif logged_in_as_teacher(user):
        playable_games = Game.objects.filter(
            game_class__teacher=user.userprofile.teacher
        )
    else:
        playable_games = Game.objects.none()
    return {
        "base_url": base_url,
        "open_play_games": playable_games if user.is_authenticated else None,
    }
