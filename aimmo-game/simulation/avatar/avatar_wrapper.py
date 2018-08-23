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

    def __init__(self, player_id, initial_location, avatar_appearance):
        self.player_id = player_id
        self.location = initial_location
        self.previous_location = initial_location
        self.orientation = "north"
        self.health = 5
        self.score = 0
        self.events = []
        self.avatar_appearance = avatar_appearance
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

    def _construct_action(self, action_data):
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

    def decide_action(self, serialised_action):
        try:
            action = self._construct_action(serialised_action)

        except (KeyError, ValueError) as err:
            LOGGER.error('Bad action data supplied: %s', err)
        except TypeError as err:
            LOGGER.error('Worker data not received: %s', err)
        else:
            self._action = action
            return True

        # Returning False here means that the action won't be registered on the cell
        # (although it will be registered on the avatar)
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
            'health': self.health,
            'location': self.location.serialise(),
            'score': self.score,
            'id': self.player_id,
            'orientation': self.orientation
        }

    def __repr__(self):
        return 'Avatar(id={}, location={}, health={}, score={})'.format(self.player_id,
                                                                        self.location,
                                                                        self.health,
                                                                        self.score)
