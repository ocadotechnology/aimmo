"""
Any helper functions used for game creation.
"""
from __future__ import absolute_import

import os

from aimmo.models import Avatar, Game


def create_game(main_user, form):
    """
    Creates a Game by:
    - saving the form
    - setting default values
    - adding users who can play the game
    - creating an avatar for the main user.

    :param main_user: The user who requested game creation, and is the game owner.
    :param form: The form used to submit the creation of the game.
    :param users_to_add_to_game: List of User objects who are able to play this game.
    :return: The initialised Game object.
    """
    game = form.save(commit=False)
    game.generator = "Main"
    game.owner = main_user
    game.main_user = main_user
    game.save()
    create_avatar_for_user(main_user, game.id)
    return game


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
