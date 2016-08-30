import logging
import requests

from simulation import game_settings
from simulation.action import ACTIONS, WaitAction

LOGGER = logging.getLogger(__name__)


class AvatarWrapper(object):
    """
    The application's view of a character, not to be confused with "Avatar",
    the player-supplied code.
    """

    def __init__(self, user_id, initial_location, worker_url, appearance):
        self.user_id = user_id
        self.location = initial_location
        self.health = game_settings.AVATAR_STARTING_HEALTH
        self.score = 0
        self.events = []
        self.appearance = appearance
        self.worker_url = worker_url
        self.fog_of_war_modifier = 0

    def _fetch_action(self, state_view):
        return requests.post(self.worker_url, json=state_view).json()

    def _construct_action(self, data):
        action_data = data['action']
        action_type = action_data['action_type']
        action_args = action_data.get('options', {})
        action_args['avatar'] = self.user_id
        action_args['origin'] = self.location
        return ACTIONS[action_type](**action_args)

    def decide_action(self, state_view):
        try:
            data = self._fetch_action(state_view)
            action = self._construct_action(data)

        except (KeyError, ValueError) as err:
            LOGGER.info('Bad action data supplied: %s', err)
        except requests.exceptions.ConnectionError:
            LOGGER.info('Could not connect to worker, probably not ready yet')
        except Exception:
            LOGGER.exception('Unknown error while fetching turn data')

        else:
            return action

        return WaitAction(self)

    def add_event(self, event):
        self.events.append(event)

    def snapshot(self):
        return {
            'id': self.user_id,
            'x': self.location.x,
            'y': self.location.y,
            'health': self.health,
            'score': self.score,
            'rotation': 0,
            'colours': {
                "bodyStroke": "#0ff",
                "bodyFill": "#%06x" % (self.user_id * 4999),  # TODO: implement better colour functionality.
                "eyeStroke": "#aff",
                "eyeFill": "#eff",
            }
        }

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
        return 'Avatar(id={}, location={}, health={}, score={})'.format(
            self.user_id, self.location, self.health, self.score
        )
