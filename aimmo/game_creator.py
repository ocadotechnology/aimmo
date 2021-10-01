
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
