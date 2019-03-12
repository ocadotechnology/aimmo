# Effects

Effects are a component of an `Interactable`.

An effect should have at least one target, the only exception is the delete `effect`, which currently always effects the `Interactable` it belongs to and thus does not need a target.
When an Interactable's conditions are met, the targets are gathered, and the effects are then given to them. Targets for an effect must have a `effect` attribute with which to store its active effects.

An effect can last 1 or many turns, and can impart a temporary or permanent change to its target, for example: restoring some of an Avatar's health, or giving an avatar a temporary damage boost.
