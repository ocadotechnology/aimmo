# Worker Manager

---

The worker has the following responsibilities:
* Creating new workers
* Deleting old workers
* Updating worker code

By worker, we are referring to the thread (in local mode) or pod (in k8s mode) that actually runs the player's code. Note that there is a difference between avatars (represented in the game as `AvatarWrapper`) and a worker.
The first is a representation in the simulation only, while the latter represents the thread / pod. It is important that `WorkerManager` has no interaction with simulation logic. 


Adding workers is done in a concurrent manner, using a pool of [green threads](https://en.wikipedia.org/wiki/Green_threads). This is because the creation of workers often involves expensive io. Methods in `WorkerManager` (and its subclasses) must be thread safe. 

Removing and adding workers is done in two different ways locally and on the cloud. Locally, we use threads, each running on different pods. With Kubernetes, we create and remove pods manually. 
