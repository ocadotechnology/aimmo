from logging import getLogger

from simulation.direction import Direction
from simulation.event import FailedAttackEvent
from simulation.event import FailedMoveEvent
from simulation.event import MovedEvent
from simulation.event import PerformedAttackEvent
from simulation.event import ReceivedAttackEvent
from simulation.game_settings import DEFAULT_ATTACK_DAMAGE

LOGGER = getLogger(__name__)


class Action(object):
    def __init__(self, avatar_id, source, direction=None):
        self._avatar_id = avatar_id
        self._source = source
        self._direction = direction

    @property
    def avatar_id(self):
        return self._avatar_id

    @property
    def source(self):
        return self._source

    @property
    def direction(self):
        return self._direction

    @property
    def target(self):
        return self._source + self._direction

    def process(self, game_state, other_actions):
        if self.is_legal(game_state, other_actions):
            self.apply(game_state, other_actions)
        else:
            self.reject(game_state)

    def is_legal(self, game_state, other_actions):
        raise NotImplementedError('Abstract method')

    def apply(self, game_state, other_actions):
        raise NotImplementedError('Abstract method')

    def reject(self, game_state):
        raise NotImplementedError('Abstract method')


class WaitAction(Action):
    def __init__(self, avatar, source):
        Action.__init__(self, avatar, source)

    def is_legal(self, game_state, other_actions):
        return True

    def apply(self, game_state, other_actions):
        pass


class MoveAction(Action):
    def __init__(self, avatar, source, direction_dict):
        # Untrusted data!
        direction = Direction.from_dict(direction_dict)
        Action.__init__(self, avatar, source, direction)

    def process(self, game_state, other_actions):
        self.chain(game_state, other_actions, {self.source})

    def chain(self, game_state, other_actions, visited):
        if not self.is_legal(game_state, other_actions):
            return self.reject(game_state)

        # Detect cycles
        if self.target in visited:
            return self.reject(game_state)

        if not game_state.cell_occupied(self.target):
            return self.apply(game_state, other_actions)

        next_avatar = game_state.avatar_at(self.target)
        next_action = other_actions.by_avatar(next_avatar)
        if next_action.chain(game_state, other_actions, visited | {self.target}):
            return self.apply(game_state, other_actions)

        return self.reject(game_state)

    def is_legal(self, game_state, other_actions):
        if not game_state.cell_habitable(self.target):
            return False

        if other_actions.num_moves_to(self.target) > 1:
            return False

        if not game_state.cell_occupied(self.target):
            return True

        avatar_id = game_state.avatar_at(self.target)

        return other_actions.avatar_moving(avatar_id)

    def apply(self, game_state, other_actions):
        game_state.move_avatar(self.avatar_id, self.direction)
        game_state.add_event(self.avatar_id, MovedEvent(self.source, self.target))
        return True

    def reject(self, game_state):
        game_state.add_event(self.avatar_id, FailedMoveEvent(self.source, self.target))
        return False


class AttackAction(Action):
    def __init__(self, avatar, source, direction_dict):
        # Untrusted data!
        direction = Direction.from_dict(direction_dict)
        Action.__init__(self, avatar, source, direction)

    def _attacked_avatar(self, game_state, other_actions):
        if game_state.cell_occupied(self.target):
            return game_state.avatar_at(self.target)

        if other_actions.num_moves_to(self.target) == 1:
            return other_actions.moves_to(self.target)[0].avatar_id

        return None

    def is_legal(self, game_state, other_actions):
        return self._attacked_avatar(game_state, other_actions) is not None

    def apply(self, game_state, other_actions):
        attacked_avatar = self._attacked_avatar(game_state, other_actions)

        damage = DEFAULT_ATTACK_DAMAGE
        game_state.hurt_avatar(attacked_avatar, damage)
        game_state.add_event(self.avatar_id, PerformedAttackEvent(attacked_avatar, self.target, damage))
        game_state.add_event(attacked_avatar, ReceivedAttackEvent(self.avatar_id, damage))

        LOGGER.debug(
            'Avatar {} dealt {} damage to avatar {}'.format(
                self.avatar_id,
                damage,
                attacked_avatar
            )
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
