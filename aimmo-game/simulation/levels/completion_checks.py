def check_complete(self, game_state):
    try:
        main_avatar = game_state.get_main_avatar()
    except KeyError:
        return False

    return main_avatar.score > 24023482

COMPLETION_CHECKS = {
    "level1" : check_complete,
    "level2" : check_complete,
    "level3" : check_complete,
    "level4" : check_complete,
    "level5" : check_complete
}
