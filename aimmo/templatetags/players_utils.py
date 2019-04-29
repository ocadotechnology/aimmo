from django import template

register = template.Library()


@register.inclusion_tag("players/dropdown.html", takes_context=True)
def game_dropdown_list(context, base_url):
    return get_user_playable_games(context, base_url)


def get_user_playable_games(context, base_url):
    user = context.request.user
    return {
        "base_url": base_url,
        "open_play_games": user.playable_games.all()
        if user.is_authenticated()
        else None,
    }
