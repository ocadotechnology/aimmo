from django import template

from players import app_settings
from players.models import Game

register = template.Library()


@register.inclusion_tag('players/dropdown.html', takes_context=True)
def game_dropdown_list(context, base_url):
    return {
        'base_url': base_url,
        'open_play_games': Game.objects.for_user(context.request.user).filter(levelattempt=None),
        'level_numbers': xrange(1, app_settings.MAX_LEVEL+1),
    }
