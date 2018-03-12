# Architecture

This section describes the whole game architecture and how things are structured. AI:MMO consists of four main components, split into their own directories.

---

## Components

[The UI (`players` directory)](...) 

A Django app used for the front-end and database interaction (one globally). There are static Unity build files to render the game in browser.

[Games (`aimmo-game` directory)](...)

Holds and updates the game state (one per game).

[Game Creator (`aimmo-game-creator` directory)](...)

Responsible for creating games (one globally).

[Workers (`aimmo-game-worker` directory)](...)

Contains the code for an avatar which is given a game state and returns the avatar's action for that turn.

## Terminology

**Avatar:** a player's in-game representation. A player can have up to one per game.

**Player:** a single person with an account.

