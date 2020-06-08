# Simulation Runner

The [`SimulationRunner`](simulation-runner-file) is responsible
for running a turn in the simulation.

The `run_turn` method is called from `GameRunner`, and it
runs as follows:

- Get the [`AvatarWrapper`'s](avatar-wrapper-file) to
  deserialize and register their actions.
- Update the environment using the [World Map](world-map-doc)
- Check if the level is complete (the MMO will probably not
  finish - this is a somewhat deprecated feature)

The alternatives for pooling each avatar for its decisions are:

- SequentialTurnManager (used locally for testing) - get and
  apply each avatar's action in turn
- ConcurrentTurnManager - concurrently get the intended
  actions from all avatars and register them on the world map;
  then apply actions in order of priority

[simulation-runner-file]: /aimmo-game/simulation/simulation_runner.py
[avatar-wrapper-file]: /aimmo-game/simulation/avatar/avatar_wrapper.py
[world-map-doc]: world-map.md
