class AvatarWrapper(object):
    """
    The application's view of a character, not to be confused with "Avatar", the player-supplied code.
    """

    def __init__(self, initial_location, player_id, worker_url, avatar_appearance):
        self.location = initial_location
        self.health = 5
        self.score = 0
        self.events = []
        self.player_id = player_id
        self.avatar_appearance = avatar_appearance
        self.worker_url = worker_url


    def die(self, respawn_location):
        # TODO: extract settings for health and score loss on death
        self.health = 5
        self.score = max(0, self.score - 2)
        self.location = respawn_location

    def add_event(self, event):
        self.events.append(event)

    def serialise(self):
        return {
            'events': [event.serialise() for event in self.events],
            'health': self.health,
            'location': self.location.serialise(),
            'player_id': self.player_id,  # TODO: Change this to something that doesn't expose player info
            'score': self.score,
        }

    def __repr__(self):
        return 'Avatar(id={}, location={}, health={}, score={})'.format(self.player_id, self.location,
                                                                        self.health, self.score)
