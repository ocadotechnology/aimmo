# Avatar

---

This represents an avatar as part of the simulation.

The avatar functionality is separated in several classes:

- `AvatarWrapper` - the central avatar functionality, including the simulation properties such as health, score and so on
- `AvatarView` - a personalized view of the worlds for each avatar
- `AvatarAppearance` - a data class for customising the avatar's appearance
- `AvatarManager` - a structure that maintains a mapping from player_id to `AvatarWrapper`s

### `AvatarWrapper`
The avatar wrapper represents the application's view of a character.
The main functionality is:

- decide action - given a serialised representation of an action, return a Python action object.
- clear action
- update effects - apply effects that come from getting a pickup
- add event - attaches an event to the event setting -- not yet used

*This functionality may not be fully implemented:*

- die - dies and re-spawns at new location
- damage - take damage


### `AvatarManager`
This is responsible for adding and removing avatars and managing the list of avatars that the main game simulation has a access to. It is kept in sync with the `Worker`s in [`WorkerManager`](worker-manager.md) by [`GameRunner`](game-runner.md).
