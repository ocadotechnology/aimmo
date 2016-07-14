from simulation.action import ACTIONS
import requests
import logging

LOGGER = logging.getLogger(__name__)


class AvatarWrapper(object):
    """
    The application's view of a character, not to be confused with "Avatar",
    the player-supplied code.
    """

    def __init__(self, initial_location, player_id, worker_url, avatar_appearance):
        self.location = initial_location
        self.health = 5
        self.score = 0
        self.events = []
        self.player_id = player_id
        self.avatar_appearance = avatar_appearance
        self.worker_url = worker_url
        self.effects = set()
        self.resistance = 0

    def take_turn(self, game_state, game_view):
        action = self._get_action(game_view)
        if action is not None:
            action.apply(game_state, self)
            LOGGER.debug("%s took %s" % (self.player_id, action))
        effects_to_remove = set()
        for effect in self.effects:
            if not effect.turn():
                effects_to_remove.add(effect)
        for effect in effects_to_remove:
            effect.remove()

    def _get_action(self, game_view):
        try:
            data = requests.post(self.worker_url, json=game_view).json()
        except ValueError as err:
            LOGGER.info("Failed to get turn result: %s", err)
        else:
            try:
                action_data = data['action']
                action = ACTIONS[action_data['action_type']](**action_data.get('options', {}))
            except (KeyError, ValueError) as err:
                LOGGER.info("Bad action data supplied: %s", err)
                return None
            else:
                return action

    def die(self, respawn_location):
        # TODO: extract settings for health and score loss on death
        self.health = 5
        self.score = max(0, self.score - 2)
        self.location = respawn_location

    def add_event(self, event):
        self.events.append(event)

    def damage(self, amount):
        applied_dmg = max(0, amount - self.resistance)
        self.health -= applied_dmg
        return applied_dmg

    def serialise(self):
        return {
            'events': [
                #    {
                #        'event_name': event.__class__.__name__.lower(),
                #        'event_options': event.__dict__,
                #    } for event in self.events
            ],
            'health': self.health,
            'location': self.location.serialise(),
            'score': self.score,
        }

    def __repr__(self):
        return 'Avatar(id={}, location={}, health={}, score={})'.format(self.player_id, self.location, self.health, self.score)
