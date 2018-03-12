# Game Creator (`aimmo-game-creator` directory)

---

The game creator consists only of a few classes. The service runs a worker manager daemon which periodically updates the games. The list of the games is exposed through the game API.

The data is managed by a thread-safe class called WorkerManagerData. The synchronization is done using a lock over the set of the games. The set of games will change during each periodic update. The games that are no more present in the set of games exposed by the API are getting removed. The updates are made in parallel by multiple threads, thus the need for synchronization.