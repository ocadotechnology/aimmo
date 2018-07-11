# Worker Manager

---

The worker manager runs room loop responsible for updating the user's code, user arrival and departure. It is a daemon that runs as part of the [Game](README.md) service.

The `update` method has the following responsibilities:
* Adding new users to the game. This involves creating a worker and adding a new `AvatarWrapper`.
* Propagating changes to user code. This involves deleting the old worker, updating the user code and then creating a new worker. 


*Notice there is a difference between an avatar and a worker*. The worker is a different micro-service that runs in another container and runs the user code, while the avatar is an instance of `AvatarWrapper` that is used in the game simulation. Updating the user code recreates the worker, but not the avatar.

At each update the list of users is pulled from the django game API, which retrieves the data from the database.
The code is pulled from the database again using the Django game API.

Adding users is done in a concurrent manner, using a pool of [green threads](https://en.wikipedia.org/wiki/Green_threads). 

All the WorkerManager data is handled by a class called **WorkerManagerData**. WorkerManagerData is a shared object protected by locks that encapsulates list of avatars. As the list of users is shared data and we have concurrent actions, we need a thread safe class. All the actions regarding an avatar (i.e. pulling its code, adding it to the list of avatars, etc.) are done through this class.

Removing and adding workers is done in two different ways locally and on the cloud. Locally, we use threads, each running on different pods. With Kubernetes, we create and remove pods manually. 
