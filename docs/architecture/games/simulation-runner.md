# Simulation Runner

---



The `SimulationRunner` is responsible for running a turn in the simulation. 

The `run_turn` method is called from `GameRunner`, and it runs as follows:

* Get the `AvatarWrappers` to deserialize and register their actions. 
* Update the environment using the [World Map](world-map.md)
* Check if the level is complete (the MMO will probably not finish - this is a somewhat deprecated feature) 

The alternatives for pooling each avatar for its decisions are:
* SequentialTurnManager (used locally for testing) - get and apply each avatar's action in turn 
* ConcurrentTurnManager - concurrently get the intended actions from all avatars and register them on the world map; then apply actions in order of priority


