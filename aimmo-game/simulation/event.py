from collections import namedtuple

ReceivedAttackEvent = namedtuple("ReceivedAttackEvent", ["attacking_avatar", "damage_dealt"])

PerformedAttackEvent = namedtuple("PerformedAttackEvent", ["attacked_avatar", "target_location", "damage_dealt"])

FailedAttackEvent = namedtuple("FailedAttackEvent", ["target_location"])

MovedEvent = namedtuple("MovedEvent", ["source_location", "target_location"])

FailedMoveEvent = namedtuple("FailedMoveEvent", ["source_location", "target_location"])

PickedUpEvent = namedtuple("PickedUpEvent", ["interactable"])

FailedPickupEvent = namedtuple("FailedPickupEvent", [])

DroppedEvent = namedtuple("DroppedEvent", ["index"])

FailedDropEvent = namedtuple("FailedDropEvent", [])
