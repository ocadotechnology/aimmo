# Structure

Here we will go into some detail on how Babylon is structured within our project, and how we've chosen to organise the files.

---

First, we will look at the file structure for the babylon part of the game page:
```
babylon
│
├── entities
│   ├── avatarManager.test.ts
│   ├── avatarManager.ts
│   ├── index.ts
│   ├── interactableManager.test.ts
│   ├── obstacleManager.test.ts
│   └── obstacleManager.ts
│
├── environment
│   ├── camera.test.ts
│   ├── camera.ts
│   ├── environment.ts
│   ├── environmentManager.ts
│   ├── index.ts
│   ├── light.test.ts
│   ├── light.ts
│   └── terrain.ts
│
├── animation.ts
├── diff.test.ts
├── diff.ts
├── interfaces.test.ts
├── interfaces.ts
└── orientation.ts
```
`interfaces.ts` contains the typing (interfaces) for objects specific to our project, such as [GameNode](../gamenode/README.md#GameNode), [DiffHandling](../diff/README.md##DiffHandling) and [DiffProcessor](../diff/README.md##DiffProcessor)

We split the remaining elements of the game into two folders: 
* **entities**: These populate the game world, and cover elements such as obstacles, avatars, and interactables.
* **environment**: The elements of the game that make up the world, such as camera, light and terrain, as well as the renderer.

All classes in these folders implement the [GameNode](../gamenode/README.md#GameNode) interface. Entities also implement the [DiffHandling](../diff/README.md#DiffHandling) interface.