# Games (`aimmo-game` directory)

---

## Game Components
- [Game Runner](game-runner.md)
- [Worker Manager](worker-manager.md) 
- [Simulation Runner](simulation-runner.md) 
- [Worker](worker.md)
- [Map Generator](generators.md) 
- [World Map](world-map.md)
- [Avatar](avatar.md) 
- [Actions](actions.md) 
- [Pickups](pickups.md) 



## In Short
- Maintains game state
- Simulates environment events
- Runs player actions

## General Overview
Each game has its own instance of a game container. The game 
container is responsible for maintaining the game state, 
the worker avatars for the game, fetching the actions from 
each worker, and applying those actions, as well as fetching 
game metadata from the Django API.

The game interacts with the rest of the components as follows:
- It is created by the game creator.
- It creates workers and deletes them as dictated by the game 
state
- It exposes an [API](game-api) to provide the workers with the code.
- It fetches the game settings from the UI.

Once per turn it will:
- Inform all workers of the current game state and gets their 
actions.
- Perform conflict resolution on these actions and then apply 
them.
- Update the world with any other changes (eg move score 
squares).

Files for the game are stored in `aimmo-game`.

[game-api]: https://github.com/ocadotechnology/aimmo/blob/master/aimmo-game/service.py
