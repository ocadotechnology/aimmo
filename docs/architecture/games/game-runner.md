# Game Runner

---

The `GameRunner` has the following responsibilities:
    
* Run the main game loop. In the main game loop, it does the following:
1. Fetch the game metadata (i.e. the players)
2. From this, figure out what players need to be added and removed. 
3. Tell the `WorkerManager` to add / remove the appropriate workers.
4. Tell the `AvatarManager` to add / remove the appropriate avatars. 

The `GameRunner` is the **only** class which has interactions with both *simulation logic* (avatar wrappers, game map etc) and *worker logic* (`WorkerManager`). This is an important decoupling. 

