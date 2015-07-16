from collections import namedtuple

ReceivedAttackEvent = namedtuple('ReceivedAttackEvent', ['attacking_player', 'damage_dealt'])

PerformedAttackEvent = namedtuple('PerformedAttackEvent', ['attacked_player', 'target_location', 'damage_dealt'])

FailedAttackEvent = namedtuple('FailedAttackEvent', ['target_location'])

MovedEvent = namedtuple('MovedEvent', ['source_location', 'target_location'])

FailedMoveEvent = namedtuple('FailedMoveEvent', ['source_location', 'target_location'])
