from logging import getLogger

from simulation.direction import Direction
from simulation.event import FailedAttackEvent, FailedMoveEvent, MovedEvent, PerformedAttackEvent, ReceivedAttackEvent
from simulation.game_settings import DEFAULT_ATTACK_DAMAGE

LOGGER = getLogger(__name__)


class Action(object):
    def __init__(self, avatar, origin, direction=None):
        self._avatar = avatar
        self._origin = origin
        self._direction = direction

    @property
    def avatar(self):
        return self._avatar

    @property
    def avatar_id(self):
        return self._avatar.user_id

    @property
    def origin(self):
        return self._origin

    @property
    def direction(self):
        return self._direction

    @property
    def target(self):
        return self._origin + self._direction

    def process(self, game_state, other_actions=None):
        if self.is_legal(game_state, other_actions):
            self.apply(game_state, other_actions)
        else:
            self.reject(game_state)

    def is_legal(self, game_state, other_actions=None):
        raise NotImplementedError('Abstract method')

    def apply(self, game_state, other_actions):
        raise NotImplementedError('Abstract method')

    def reject(self, game_state):
        raise NotImplementedError('Abstract method')


class WaitAction(Action):
    def __init__(self, avatar, origin):
        Action.__init__(self, avatar, origin)

    def is_legal(self, game_state, other_actions=None):
        return True

    def apply(self, game_state, other_actions):
        pass


class MoveAction(Action):
    def __init__(self, avatar, origin, direction):
        # Untrusted data!
        Action.__init__(self, avatar, origin, direction=Direction.copy(direction))

    def process(self, game_state, other_actions=None):
        start = game_state.avatar_manager.location(self.avatar_id)
        self.chain(game_state, other_actions, {start})

    def chain(self, game_state, other_actions, visited):
        if not self.is_legal(game_state, other_actions):
            return self.reject(game_state)

        # Detect cycles
        if self.target in visited:
            return self.reject(game_state)

        if not game_state.world_map.cell_occupied(self.target):
            return self.apply(game_state, other_actions)

        next_avatar = game_state.avatar_at(self.target)
        next_action = other_actions.by_avatar(next_avatar)
        if next_action.chain(game_state, other_actions, visited | {self.target}):
            return self.apply(game_state, other_actions)

        return self.reject(game_state)

    def is_legal(self, game_state, other_actions=None):
        world = game_state.world_map

        if not world.cell_habitable(self.target):
            return False

        if (other_actions is not None
                and other_actions.num_moves_to(self.target) > 1):
            return False

        if not world.cell_occupied(self.target):
            return True

        avatar_id = game_state.avatar_at(self.target)

        return (other_actions is not None
                and other_actions.avatar_moving(avatar_id))

    def apply(self, game_state, other_actions):
        game_state.move_avatar(self.avatar_id, self.direction)
        game_state.add_event(self.avatar_id, MovedEvent(self.origin, self.target))

        new_cell = game_state.world_map.get_cell(self.target)
        if new_cell.pickup:
            # TODO:  extract pickup logic into pickup when adding multiple types
            self.avatar.health = min(10, self.avatar.health + new_cell.pickup.health_restored)
            new_cell.pickup = None

        return True

    def reject(self, game_state):
        game_state.add_event(self.avatar_id, FailedMoveEvent(self.origin, self.target))
        return False


class AttackAction(Action):
    def __init__(self, avatar, origin, direction):
        #                                               Untrusted data!
        Action.__init__(self, avatar, origin, direction=Direction.copy(direction))

    def _attacked_avatar(self, game_state, other_actions):
        if game_state.cell_occupied(self.target):
            return game_state.avatar_at(self.target)
        elif (other_actions is not None
              and other_actions.num_moves_to(self.target) == 1):
            return other_actions.moves_to(self.target)[0].avatar_id
        else:
            return None

    def is_legal(self, game_state, other_actions=None):
        return self._attacked_avatar(game_state, other_actions) is not None

    def apply(self, game_state, other_actions):
        attacked_avatar = self._attacked_avatar(game_state, other_actions)

        damage = DEFAULT_ATTACK_DAMAGE
        game_state.hurt_avatar(attacked_avatar, damage)
        game_state.add_event(self.avatar_id, PerformedAttackEvent(attacked_avatar, self.target, damage))
        game_state.add_event(attacked_avatar, ReceivedAttackEvent(self.avatar_id, damage))

        LOGGER.debug(
            '{} dealt {} damage to {}'.format(self.avatar, damage, attacked_avatar)
        )

    def reject(self, game_state):
        game_state.add_event(self.avatar_id, FailedAttackEvent(self.target))

ACTIONS = {
    'attack': AttackAction,
    'move': MoveAction,
    'wait': WaitAction,
}

PRIORITIES = {
    WaitAction: 0,
    AttackAction: 1,
    MoveAction: 2,
}
