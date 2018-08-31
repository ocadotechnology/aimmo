# Game Runner

---
The code can be found [here](game runner update).

The `GameRunner` class is responsible for initialising the
games' components in order to spawn a new game. It holds a 
reference to these objects and has some getter functions 
defined in order to spawn or delete new users.

More importantly, it contains the `update()` function which
runs in a loop at `WORKER_UPDATE_SLEEP_TIME` intervals. This
constantly uses the embedded communicator object to get
the game metadata from our django API url.

Once this information comes in it manages the changes in 
users that needs to happen (ie. finds users that need to 
be added or deleted). It then delegates the responsibility
to the worker manager which handles the worker pods & their
code. Finally the game state holds all new avatars for these 
users. 

The `GameRunner` should be the **only** class which has 
interactions with both *simulation logic* (avatar wrappers, 
game map etc) and *worker logic* (`WorkerManager`). This is 
an important decoupling. 

[game runner update]: https://github.com/ocadotechnology/aimmo/blob/d61c3f575f012fc6f99da9a99a4e5b3ac461d65c/aimmo-game/simulation/game_runner.py#L30

