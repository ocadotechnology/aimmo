# Worker

---

When we refer to a worker we are referring to a thread or
a kubernetes containerised pod. The isn't part of the game 
logic but ensures that the game can receive and receive 
external data safely.

The responsibilities include:
* Stores worker data not directly to the simulation: logs, 
serialised actions and code updated flags.
* Fetches data from the remote service (thread / pod)
