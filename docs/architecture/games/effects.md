# Effects

Effects are a component of an `Interactable`.

An effect must have a target, the only exception is the delete effect, which can currently only effect the `Interactable` it belongs to.
When an Interactable's conditions are met, the targets are found, and the effects are then given to them. Targets for an effect must have a `effectz attribute with which to store it's active effects.

An effect can last 1 or many turns, and can impart a temporary or permenant change to it's target, for example: restoring some of an Avatar's health, or giving an avatar a temporary damage boost.