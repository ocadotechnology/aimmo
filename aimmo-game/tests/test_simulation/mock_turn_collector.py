from turn_collector import TurnCollector, CollectedTurnActions


class MockTurnCollector(TurnCollector):
    def __init__(self):
        self.collected_turn_actions = CollectedTurnActions(0)
