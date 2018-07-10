from django import template

from aimmo import app_settings

register = template.Library()


@register.inclusion_tag('players/dropdown.html', takes_context=True)
def game_dropdown_list(context, base_url):
    user = context.request.user
    return {
        'base_url': base_url,
        'open_play_games': user.playable_games.all() if user.is_authenticated() else None,
        'level_numbers': xrange(1, app_settings.MAX_LEVEL+1),
    }
