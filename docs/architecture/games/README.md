# Games (`aimmo-game` directory)

## Game Components

- [Game Runner](game-runner.md)
- [Simulation Runner](simulation-runner.md)
- [Map Generator](generators.md)
- [World Map](world-map.md)
- [Avatar](avatar.md)
- [Actions](actions.md)
- [Pickups](pickups.md)
- [Interactables](interactable.md)

## In Short

- Maintains game state
- Simulates environment events
- Collects and runs player actions

## General Overview

The game (aimmo-game) is responsible for maintaining the game state,
the worker avatars for the game, fetching the actions from
each worker, and applying those actions, as well as fetching
game metadata from the Django API.

The game interacts with the rest of the components as follows:

- It is created by the game creator.
- Collects actions (see [turn_collector](../../../aimmo-game/turn_collector.py)) computed by the player's client (see [workers](../workers/README.md))
- Send game states once per turn to the clients

Once per turn it will:

- Inform all workers of the current game state and gets their
  actions.
- Perform conflict resolution on these actions and then apply
  them.
- Update the world with any other changes (eg move score
  squares).

Files for the game are stored in `aimmo-game`.

[game-api]: https://github.com/ocadotechnology/aimmo/blob/master/aimmo-game/service.py
