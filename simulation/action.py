from event import *
import world_map as world_map_module


class Action(object):
    def apply(self, world_state, avatar):
        raise NotImplementedError('Abstract method')


class WaitAction(Action):
    def apply(self, world_state, avatar):
        _add_score_from_cell_if_needed(avatar, world_state)


class MoveAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, avatar):
        target_location = avatar.location + self.direction
        if world_state.world_map.can_move_to(target_location):
            avatar.add_event(MovedEvent(avatar.location, target_location))
            world_state.world_map.get_cell(avatar.location).avatar = None
            avatar.location = target_location
            new_cell = world_state.world_map.get_cell(target_location)
            new_cell.avatar = avatar
            if new_cell.pickup:
                # TODO: potentially extract pickup logic into pickup when adding multiple types
                avatar.health = min(10, avatar.health + new_cell.pickup.health_restored)
                new_cell.pickup = None
        else:
            avatar.add_event(FailedMoveEvent(avatar.location, target_location))
        _add_score_from_cell_if_needed(avatar, world_state)


class AttackAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, avatar):
        target_location = avatar.location + self.direction
        attacked_avatar = world_state.world_map.get_cell(target_location).avatar
        if attacked_avatar:
            damage_dealt = 1
            avatar.add_event(PerformedAttackEvent(attacked_avatar, target_location, damage_dealt))
            attacked_avatar.add_event(ReceivedAttackEvent(avatar, damage_dealt))
            attacked_avatar.health -= damage_dealt
            print('{} dealt {} damage to {}'.format(avatar, damage_dealt, attacked_avatar))
            if attacked_avatar.health <= 0:
                respawn_location = world_state.world_map.get_random_spawn_location()
                attacked_avatar.die(respawn_location)
                world_state.world_map.get_cell(target_location).avatar = None
                world_state.world_map.get_cell(respawn_location).avatar = attacked_avatar
        else:
            avatar.add_event(FailedAttackEvent(target_location))
        _add_score_from_cell_if_needed(avatar, world_state)


# TODO: investigate moving this to after an action is handled - it is not specific to an action
def _add_score_from_cell_if_needed(avatar, world_state):
    cell = world_state.world_map.get_cell(avatar.location)
    if cell.generates_score:
        avatar.score += 1
