# Pickups

---

A pickup is an object that is automatically grabbed by avatars in the same cell as the pickup. The pickup gets destroyed and generates an effect it is grabbed. An effect is an object that encapsulates a function that gets applied to an avatar on each turn. (see [Turn Manager](turn-manager))

#### Pickups 

A Pickup is attached to a cell. Getting a pickup should attach an effect to an avatar. Once the pickup is attached to the avatar, it gets deleted.

The pickup references the cell and the cell references the pickup. The delete function is called once the pickup gets applied, removing both references. The Pickup class is an abstract one, each Pickup concrete class having to implement an `_apply` function.

The different types of pickup supported are:
* Health Pickup 
    * restores health immediately, no **Effect** is used
* Invulnerability Pickup 
    * an **effect-based pickup**
    * applies an InvulnerabilityPickupEffect 
* Damage Pickup
    * an **effect-based pickup**
    * applies a DamagePickupEffect 

#### Effects

An Effect is a class that gets applied once per turn. The effect interface consists of the function `on_turn` which gets applied each turn.

A Timed Effect is an Effect that gets removed after a number of turns. The Effect interface is extended with the `remove` function, that only removes the effect by default - this is overrided by different effects.

There are 2 concrete effects implemented at the moment:
* InvulnerabilityPickupEffect - increases the resistance of the avatar by a big offset
* DamagePickupEffect - adds a damage boosts when initialized, removes the damage boost at effect removal