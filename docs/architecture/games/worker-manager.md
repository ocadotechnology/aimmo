# Worker Manager

---

The worker manager runs room loop responsible for updating the user's code, user arrival and departure. It is a daemon that runs as part of the [Game](Game) service.

The loop runs as follows:
* remove the users with different code
* add missing users
* delete extra users: i.e. users that have no code
* update main avatar -- obsolete, see [Flask Microservice](flask-microservice)

At each update the list of users is pulled from the [Django game API](game-api), which retrieves the data from the database.

**Adding users**(function called spawn) is a central part of the work-flow. A user is added as follows:
* kill the old [Worker](worker)
* pull the code from the database
* add a new Worker (with the new code)
* add the **avatar** back into the game 

Adding users is done in parallel, using a pool of [green threads](https://en.wikipedia.org/wiki/Green_threads). Notice there is a difference between an avatar and a worker. The worker is a different micro-service that runs in another container and runs the user code, while the avatar is a model as part of the game simulation. The code is pulled from the database again using the Django game API.

All the WorkerManager data is handled by a class called **WorkerManagerData**. WorkerManagerData is a shared object protected by locks that encapsulates list of avatars. As the list of users is shared data and we have concurrent actions, we need a thread safe class. All the actions regarding an avatar (i.e. pulling its code, adding it to the list of avatars, etc.) are done through this class.

Removing and adding workers is done in two different ways locally and on the cloud. Locally, we use threads, each running on different pods. With Kubernetes, we create and remove pods manually. This is intended to be replaced with deployments in [pull request 150](https://github.com/ocadotechnology/aimmo/pull/150).