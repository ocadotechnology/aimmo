import logging
import requests

from simulation.action import ACTIONS, MoveAction, WaitAction
from simulation.direction import Direction, NORTH, EAST, WEST, SOUTH

LOGGER = logging.getLogger(__name__)


class AvatarWrapper(object):
    """
    The application's view of a character, not to be confused with "Avatar",
    the player-supplied code.
    """

    def __init__(self, player_id, initial_location, worker_url, avatar_appearance):
        self.player_id = player_id
        self.location = initial_location
        self.previous_location = initial_location
        self.orientation = "north"
        self.health = 5
        self.score = 0
        self.events = []
        self.avatar_appearance = avatar_appearance
        self.worker_url = worker_url
        self.effects = set()
        self.resistance = 0
        self.attack_strength = 1
        self.fog_of_war_modifier = 0
        self._action = None

    def update_effects(self):
        effects_to_remove = set()
        for effect in self.effects:
            effect.on_turn()
            if effect.is_expired:
                effects_to_remove.add(effect)
        for effect in effects_to_remove:
            effect.remove()

    @property
    def action(self):
        return self._action

    @property
    def is_moving(self):
        return isinstance(self.action, MoveAction)

    def _fetch_action(self, state_view):
        response = requests.post(self.worker_url, json=state_view).json()
        response.raise_for_status()
        return response

    def _construct_action(self, data):
        action_data = data['action']
        action_type = action_data['action_type']
        action_args = action_data.get('options', {})
        action_args['avatar'] = self
        return ACTIONS[action_type](**action_args)

    def calculate_orientation(self):
        """
        Calculates the orientation of the avatar (ie. what direction the avatar is pointed
        towards) for rendering in the front end of the game.
        :return: A string representation of a cardinal direction.
        """
        _current_location = self.location
        _previous_location = self.previous_location

        direction_of_orientation = Direction(_current_location.x - _previous_location.x,
                                             _current_location.y - _previous_location.y)

        if _current_location == _previous_location:
            return self.orientation

        return direction_of_orientation.cardinal

    def decide_action(self, state_view):
        try:
            data = self._fetch_action(state_view)
            action = self._construct_action(data)

        except (KeyError, ValueError) as err:
            LOGGER.info('Bad action data supplied: %s', err)
        except requests.exceptions.ConnectionError:
            LOGGER.info('Could not connect to worker, probably not ready yet')
        except Exception:
            LOGGER.exception("Unknown error while fetching turn data")

        else:
            self._action = action
            return True

        self._action = WaitAction(self)
        return False

    def clear_action(self):
        self._action = None

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
        return 'Avatar(id={}, location={}, health={}, score={})'.format(self.player_id,
                                                                        self.location,
                                                                        self.health,
                                                                        self.score)
