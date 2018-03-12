# Turn Manager

---

The Turn Manger is a Daemon that runs in parallel with [Worker Manager](worker-manager.md). While the purpose of the worker manager is to supervise the game room, the turn manager handles the actual simulation of the game. It is the "game loop".

The Turn Manager runs as follows:
* ask each avatar for its decision
* update the environment using the [World Map](world-map.md)
* run a callback at the end of each turn (the callback registered in the service is sending the world updates through the socket)
* check if the level is complete (the MMO will probably not finish) 

The alternatives for pooling each avatar for its decisions are:
* SequentialTurnManager - get and apply each avatar's action in turn
* ConcurrentTurnManager - concurrently get the intended actions from all avatars and register them on the world map; then apply actions in order of priority

Using one or the other turn manager impacts the game-play. For a sequential turn manager you are sure that your action is going the be applied if it is correct in accordance with the world you see(as a worker). For a concurrent turn manager, as multiple players might intend to go(or, more generally, apply an action) to a single cell, the game becomes more complex from the user point of view.

The avatars are asked for their decisions by calling the Game API. The environment is updated by calling [World Maps's methods](world-map.md), which are provided by the state provider. 
