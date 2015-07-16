class TurnManager(object):
    def __init__(self, world_state, player_manager):
        self.world_state = world_state
        self.player_manager = player_manager
        self.world_state.player_manager = player_manager

    def _update_environment(self):
        pass

    def run_turn(self):
        self._update_environment()

        actions = [(p, p.handle_turn(self.world_state.get_state_for(p))) for p in self.player_manager.players]
        for player, action in actions:
            action.apply(self.world_state, player)

    def run_game(self):
        while True:
            self.run_turn()
