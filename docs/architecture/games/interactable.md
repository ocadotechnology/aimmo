# Interactable

An `Interactable` is a dynamic object that exists in the `WorldMap`.

All Interactables follow the same basic logic:
CONDITIONS &rarr; EFFECTS &rarr; TARGETS

This is to say that an `Interactable` has 1 or more [conditions](conditions.md) it's checking for. Once the conditions are met, it will apply any [effects](effects.md) it has to 1 or more specified targets. Currently the only compatible target is an avatar.

## Implementation

When implementing a new `Interactable` there is a number of criteria that need to be met:

1. Any and all conditions should be specified in the `__init__()` method.

2. Any and all effects should be specified in the `__init__()` method.

3. The `get_targets()` method should be implemented to return a list of targets. Each effect will happen to **EVERY** target in the list.

4. It should implement a `__repr__()` and `serialize()` method for informative purposes.