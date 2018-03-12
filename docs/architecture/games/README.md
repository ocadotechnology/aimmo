# Games (`aimmo-game` directory)

---

## Game Components
- [Avatar](FAQ.md) 
- [Action](FAQ.md) 
- [Map Generator](FAQ.md) 
- [Pickups](FAQ.md) 
- [Turn Manager](FAQ.md) 
- [Worker Manager](FAQ.md) 
- [World Map](FAQ.md)

## In Short
- Maintains game state
- Simulates environment events
- Runs player actions

## General Overview
Each game has its own instance of a game container. The game container is responsible for maintaining the game state, 
the worker avatars for the game, fetching the actions from each worker, and applying the worker.

The game interacts with the rest of the components as follows:
- It is created by the game creator.
- It creates workers and restarts them when a user changes their avatar's code.
- It exposes an API to provide the workers with the code.
- It fetches the game settings from the UI.

Once per turn it will:
- Inform all workers of the current game state and gets their actions.
- Perform conflict resolution on these actions and then apply them.
- Update the world with any other changes (eg move score squares).

Files for the game are stored in `aimmo-game`.
