# Architecture

This section describes the whole game architecture and how things are structured. AI:MMO consists of four main components, split into their own directories.

---
The following UML diagram is intended as a rough overview of the project:
![](uml.png?raw=true)

## Components

[The UI (`aimmo` directory)](ui/README.md) 

A Django app used for the front-end and database interaction. There are static Unity build files to render the game in browser.

[Games (`aimmo-game` directory)](games/README.md)

Holds and updates the game state (one per game).

[Game Creator (`aimmo-game-creator` directory)](game-creator/README.md)

Responsible for creating games (one globally).

[Workers (`aimmo-game-worker` directory)](workers/README.md)

Contains the code for an avatar which is given a game state and returns the avatar's action for that turn.

## Terminology

**Avatar:** a player's in-game representation. A player can have up to one per game.

**Player:** an individual with an account.

