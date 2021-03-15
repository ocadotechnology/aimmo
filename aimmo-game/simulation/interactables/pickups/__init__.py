from simulation.interactables.pickups.artefact import Artefact
from simulation.interactables.pickups.yellow_orb_artefact import YellowOrbArtefact
from simulation.interactables.pickups.chest_artefact import ChestArtefact
from simulation.interactables.pickups.key_artefact import KeyArtefact
from simulation.interactables.pickups.damage_boost_pickup import DamageBoostPickup
from simulation.interactables.pickups.health_pickup import HealthPickup
from simulation.interactables.pickups.invulnerability_pickup import (
    InvulnerabilityPickup,
)


def serialize_pickups(world_map):
    return [cell.interactable.serialize() for cell in world_map.pickup_cells()]


ALL_PICKUPS = (
    DamageBoostPickup,
    InvulnerabilityPickup,
    HealthPickup,
    Artefact,
    YellowOrbArtefact,
    ChestArtefact,
    KeyArtefact,
)
