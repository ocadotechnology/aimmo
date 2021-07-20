# -*- coding: utf-8 -*-
# Code for Life
#
# Copyright (C) 2021, Ocado Innovation Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ADDITIONAL TERMS – Section 7 GNU General Public Licence
#
# This licence does not grant any right, title or interest in any “Ocado” logos,
# trade names or the trademark “Ocado” or any other trademarks or domain names
# owned by Ocado Innovation Limited or the Ocado group of companies or any other
# distinctive brand features of “Ocado” as may be secured from time to time. You
# must not distribute any modification of this program using the trademark
# “Ocado” or claim any affiliation or association with Ocado or its employees.
#
# You are not authorised to use the name Ocado (or any of its trade names) or
# the names of any author or contributor in advertising or for publicity purposes
# pertaining to the distribution of this program, without the prior written
# authorisation of Ocado.
#
# Any propagation, distribution or conveyance of this program must include this
# copyright notice and these terms. You must not misrepresent the origins of this
# program; modified versions of the program must be marked as such and not
# identified as the original program.

import secrets
from aimmo.avatar_creator import create_avatar_for_user
from aimmo.game_manager import GameManager

NUM_BYTES_FOR_TOKEN_GENERATOR = 32
TOKEN_MAX_LENGTH = 48


def generate_game_token():
    return secrets.token_urlsafe(nbytes=NUM_BYTES_FOR_TOKEN_GENERATOR)[
        :TOKEN_MAX_LENGTH
    ]


def create_game(main_user, form):
    """
    Creates a Game by:
    - saving the form
    - setting default values
    - adding users who can play the game
    - creating an avatar for the main user.
    - creating the game secret in game manager
    :param main_user: The user who requested game creation, and is the game owner.
    :param form: The form used to submit the creation of the game.
    :param users_to_add_to_game: List of User objects who are able to play this game.
    :return: The initialised Game object.
    """
    game = form.save(commit=False)
    game.auth_token = generate_game_token()
    game.generator = "Main"
    game.owner = main_user
    game.main_user = main_user
    game.save()
    create_avatar_for_user(main_user, game.id)
    game_manager = GameManager()
    game_manager.create_game_secret(game_id=game.id, token=game.auth_token)
    return game
