# Conditions

Conditions are a component of an `Interactable`.

A condition can be thought of as an expression, these expressions will be evaluated every turn. If all the conditions for an `Interactable` are found to be true, it will cause the Interactable's effect(s) to occur.

Here is an example implementation of a condition:

```python
def avatar_on_cell(cell: Cell):
    """ Returns an expression that checks if an avatar is on a specified cell """
    def condition(worldmap: WorldMap):
        return cell.avatar is not None
    return condition
```

This condition allows an `Interactable` to check for the existence of an avatar of a given cell. This approach can make applying this idea relatively simple. For example, here is this condition as used by our pickups:

```python
self.conditions.append(avatar_on_cell(cell))
```

Since any given pickup is a subclass of `Interactable` we know it contains an attribute `conditions` which is a simple list where all an Interactable's conditions should be kept. To give a pickup the ability to detect when a player is on top of it, we simply append the `avatar_on_cell` condition to the pickups list of conditions, supplying it with the cell it should be checking, in this case the cell the pickup is located on.

The `conditions_met` function then evaluates these expressions, and if all the conditions are met, the Interactable's effect(s) will trigger.

Finally, as a general pattern, conditions should follow this format:

```python
def NAME_OF_CONDITION(data required by the expression):
    """ explanation of what the condition is for. """
    def condition(worldmap: WorldMap):
        return (expression to evaluate)
    return condition
```

This allows you to make use of the same kinds of conditions in many different cases by simply supplying different data for the expression.
