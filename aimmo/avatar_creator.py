
from aimmo.models import Avatar, Game


def create_avatar_for_user(user, game_id):
    """
    Creates an Avatar object for a user. Sets the initial code to simple avatar code
    (unless specified otherwise).

    :param user: The user the Avatar is for.
    :param game_id: The id of the game in which the Avatar is created.
    :return: The initialised Avatar object.
    """
    game: Game = Game.objects.get(id=game_id)
    initial_code = game.worksheet.starter_code
    avatar = Avatar.objects.create(owner=user, code=initial_code, game_id=game_id)
    return avatar
