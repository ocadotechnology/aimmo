# Conditions

Conditions are a component of an `Interactable`.

A condition can be thought of as an function, any and all conditions must be something that can evaluate to either `True` or `False`. Each turn all of an Interactable's conditions are evaluated to see if it's effects should trigger.

Conditions will typically need some kind of data to check, conditions currently can only use information from the `WorldMap` for their checks.
