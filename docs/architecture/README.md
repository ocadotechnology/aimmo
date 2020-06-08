# Architecture

This section describes the whole game architecture and how things are structured. Kurono consists of four main components, split into their own directories.

## Overview

![aimmo architecture overview](overview.png)

## Components

[The Django API (`aimmo` directory)](ui/README.md)

A Django app used to provide an api for game and code management.

Game Frontend (`game)frontend` directory)

A React app using Babylon and Pyodide to present the game state to the player, run their code and allow them to edit it.

[Games (`aimmo-game` directory)](games/README.md)

Holds and updates the game state (one per game).

[Game Creator (`aimmo-game-creator` directory)](game-creator/README.md)

Responsible for creating games (one globally).

[Workers (`aimmo-game-worker` directory)](workers/README.md)

Contains the avatar worker api used by the AvatarWorker in the frontend.

## Terminology

**Avatar:** a player's in-game representation. A player can have up to one per game.

**Player:** an individual with an account.
