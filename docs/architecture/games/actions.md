# Actions

---

An action is a pair (avatar, location). The action is registered onto the WorldMap by being appended to a cell.

The action is processed by calling the apply function only if:
- the action is legal (see below)
- it's not rejected

The exposed interface is:

- **`apply`**
    - has to return true if event application succeeded
    - attaches an event to the avatar
- **`is_legal`**
    - returns if an action is legal from the point of view of the map
    - the action gets applied or rejected accordingly
- **`reject`**
    - attaches a (failed) event to the avatar

Each of the 3 elements of the interface are implemented differently by different types of actions.

The current types of actions as:
- **`WaitAction`**
    - wait is always legal
    - no actions get attached to the avatar
- **`MoveAction`**
    - *`is_legal`*
        - the responsibility is passed to world_map
    - *`apply`*
        - adds a move event to the avatar
        - change the avatar's world view
        - updates the map accordingly
    - *`reject`*
        - the failed event is added to the avatar
    - *overrides the processing of the action*
        - the action is chained in the action list of a cell
        - see World Map and Turn Manager for details
- **`AttackAction`**
    - *`is_legal`*
        * attacking is legal is the avatar is attackable
    * *`attack`*
        * attaches the event to the attacker avatar
        * attaches the event to the attacked avatar
        * if the attacked avatar dies it is respawned



### Legality of an Action
A `WaitAction` is always legal. A `MoveAction` is legal if and only if:
 - The square the avatar attempts to move to is on the map
 - The square the avatar attempts to move to is not occupied (by e.g. another avatar or a wall)
 - Another avatar is not attempting to move to the same square. 
 
 This means that, for example, given the following situation:
 <p style="text-align: center;"> > _ < </p>
 Where two avatars are trying to move horrizantally into the following square, we will get the following result:
  <p style="text-align: center;"> x _ x </p>gi
 Where neither of the avatars have moved.
 
 This detection of collisions is done by registering actions with the cells where the avatars attempt to move and the `detect_cycles` method in the `MoveAction` class.
 