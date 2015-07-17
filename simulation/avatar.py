class Avatar(object):
    def __init__(self, initial_location, player):
        self.location = initial_location
        self.player = player
        self.events = []

    def handle_turn(self, state):
        next_action = self.player.get_next_action(state, self.events)

        # Reset event log
        self.events = []

        return next_action

    def add_event(self, event):
        self.events.append(event)
