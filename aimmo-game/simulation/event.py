from collections import namedtuple

# Move-related:

MovedEvent = namedtuple(
    'MovedEvent',
    [
        'source_location',
        'target_location'
    ]
)

FailedMoveEvent = namedtuple(
    'FailedMoveEvent',
    [
        'source_location',
        'target_location'
    ]
)

# Attack-related:

PerformedAttackEvent = namedtuple(
    'PerformedAttackEvent',
    [
        'attacked_avatar_id',
        'target_location',
        'damage_dealt'
    ]
)

ReceivedAttackEvent = namedtuple(
    'ReceivedAttackEvent',
    [
        'attacking_avatar_id',
        'damage_dealt'
    ]
)

FailedAttackEvent = namedtuple(
    'FailedAttackEvent',
    [
        'target_location'
    ]
)

# Death-related:

DeathEvent = namedtuple(
    'DeathEvent',
    [
        'death_location',
        'respawn_location'
    ]
)