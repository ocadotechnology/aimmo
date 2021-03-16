from logging import getLogger
from typing import TYPE_CHECKING

from simulation.direction import Direction
from simulation.event import (
    FailedAttackEvent,
    FailedMoveEvent,
    FailedPickupEvent,
    MovedEvent,
    PerformedAttackEvent,
    PickedUpEvent,
    ReceivedAttackEvent,
)
from simulation.interactables.pickups.artefacts import _Artefact

if TYPE_CHECKING:
    from simulation.world_map import WorldMap
    from simulation.avatar.avatar_wrapper import AvatarWrapper

LOGGER = getLogger(__name__)


class Action(object):
    def __init__(self, avatar):
        self._avatar: "AvatarWrapper" = avatar
        try:
            self._target_location = self._avatar.location + self.direction
        except AttributeError:
            self._target_location = self._avatar.location

    @property
    def avatar(self):
        return self._avatar

    @property
    def target_location(self):
        return self._target_location

    def register(self, world_map):
        if world_map.is_on_map(self.target_location):
            world_map.get_cell(self.target_location).actions.append(self)

    def process(self, world_map):
        """Called externally to decide whether to process the action or not."""
        if self._is_legal(world_map):
            self.avatar.previous_location = self.avatar.location
            self._apply(world_map)
            self.avatar.orientation = self.avatar.calculate_orientation()
        else:
            self._reject()

    def _is_legal(self, world_map):
        raise NotImplementedError("Abstract method")

    def _apply(self, world_map: "WorldMap"):
        raise NotImplementedError("Abstract method")

    def _reject(self):
        raise NotImplementedError("Abstract method")


class WaitAction(Action):
    def __init__(self, avatar):
        super(WaitAction, self).__init__(avatar)

    def _is_legal(self, world_map):
        return True

    def _apply(self, world_map):
        self.avatar.clear_action()


class PickupAction(Action):
    def __init__(self, avatar):
        super(PickupAction, self).__init__(avatar)

    def _is_legal(self, world_map):
        current_cell = world_map.get_cell(self.avatar.location)
        cell_has_artefact = issubclass(type(current_cell.interactable), _Artefact)
        return cell_has_artefact and self.avatar.backpack_has_space()

    def _apply(self, world_map):
        current_cell = world_map.get_cell(self.avatar.location)
        current_cell.interactable.in_backpack = True
        self.avatar.add_event(PickedUpEvent(current_cell.interactable.serialize()))
        self.avatar.clear_action()

    def _reject(self):
        self.avatar.add_event(FailedPickupEvent())
        self.avatar.clear_action()
        self.avatar.logs.append(
            "Uh oh! Your avatar was unable to pick up the artefact. Your backpack is full! 🎒 "
        )


class MoveAction(Action):
    def __init__(self, avatar, direction):
        self.direction = Direction(**direction)
        super(MoveAction, self).__init__(avatar)

    def _is_legal(self, world_map):
        return world_map.can_move_to(self.target_location)

    def process(self, world_map):
        self.detect_cycles(world_map, {self.avatar.location})

    def _apply(self, world_map):
        event = MovedEvent(self.avatar.location, self.target_location)
        self.avatar.add_event(event)

        world_map.get_cell(self.avatar.location).avatar = None
        self.avatar.previous_location = self.avatar.location
        self.avatar.location = self.target_location
        self.avatar.orientation = self.avatar.calculate_orientation()
        world_map.get_cell(self.target_location).avatar = self.avatar
        self.avatar.clear_action()
        return True

    def detect_cycles(self, world_map, visited):
        if not self._is_legal(world_map):
            return self._reject()

        if self.target_location in visited:
            return self._reject()

        next_cell = world_map.get_cell(self.target_location)
        if not next_cell.is_occupied:
            return self._apply(world_map)

        next_action = next_cell.avatar.action
        if next_action.detect_cycles(world_map, visited | {self.target_location}):
            return self._apply(world_map)

        return self._reject()

    def _reject(self):
        event = FailedMoveEvent(self.avatar.location, self.target_location)
        self.avatar.add_event(event)
        self.avatar.clear_action()
        return False


class AttackAction(Action):
    def __init__(self, avatar, direction):
        self.direction = Direction(**direction)
        super(AttackAction, self).__init__(avatar)

    def _is_legal(self, world_map):
        return True if world_map.attackable_avatar(self.target_location) else False

    def _apply(self, world_map):
        attacked_avatar = world_map.attackable_avatar(self.target_location)
        damage_dealt = 1
        self.avatar.add_event(
            PerformedAttackEvent(attacked_avatar, self.target_location, damage_dealt)
        )
        attacked_avatar.add_event(ReceivedAttackEvent(self.avatar, damage_dealt))
        attacked_avatar.damage(damage_dealt)

        self.avatar.clear_action()

        if attacked_avatar.health <= 0:
            # Move responsibility for this to avatar.die() ?
            respawn_location = world_map.get_random_spawn_location()
            attacked_avatar.die(respawn_location)
            world_map.get_cell(self.target_location).avatar = None
            world_map.get_cell(respawn_location).avatar = attacked_avatar

    def _reject(self):
        self.avatar.add_event(FailedAttackEvent(self.target_location))
        self.avatar.clear_action()


ACTIONS = {
    "attack": AttackAction,
    "move": MoveAction,
    "wait": WaitAction,
    "pickup": PickupAction,
}

PRIORITIES = {WaitAction: 0, PickupAction: 0, AttackAction: 1, MoveAction: 2}
