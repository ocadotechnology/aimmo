from simulation.game_state import GameState


class MockGameState(GameState):
    turn_count = 0

    def serialize(self):
        return {"foo": "bar"}

    def get_state_for(self, avatar):
        return self
