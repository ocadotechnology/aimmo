# Avatar

---

The avatar is an interface between the worker and the managers in the simulation. It also provides a nice abstraction for what the simulation perceives as a 'user'. The avatar related functionality is grouped inside the avatar folder.

The avatar functionality is separated in several classes:

- avatar wrapper - the central avatar functionality, including the communication with the worker and the simulation properties such as health, score and so on
- avatar view - a personalized view of the worlds for each avatar
- avatar appearance - fields used only by the Raphael JS client
- the avatar manager - a structure that keeps a list of avatars. It is used by the Turn Manager to update the environment
- fog of war (currently removed, but this feature will return eventually)

### The Avatar Wrapper
The avatar wrapper represents the application's view of a character, together with an API that communicates to the worker via HTTP GETs.

The main functionality is:

- decide action - fetches an action from the worker and updates the current action to be executed
- clear action
- update effects - apply effects that come from getting a pickup
- add event - attaches an event to the event setting -- not yet used


Deciding an action is done by making a GET request to the Game API and processing the received JSON. If an error occurs during the process, a wait action is emitted.

*This functionality may not be fully implemented:*

- die - dies and respawns at new location
- damage - take damage
