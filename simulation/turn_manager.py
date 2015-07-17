class TurnManager(object):
    def __init__(self, world_state, avatar_manager):
        self.world_state = world_state
        self.avatar_manager = avatar_manager
        self.world_state.avatar_manager = avatar_manager

    def _update_environment(self):
        pass

    def run_turn(self):
        self._update_environment()

        actions = [(p, p.handle_turn(self.world_state.get_state_for(p)))
                   for p in self.avatar_manager.avatars]
        for avatar, action in actions:
            action.apply(self.world_state, avatar)

    def run_game(self):
        while True:
            self.run_turn()
