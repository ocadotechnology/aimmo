# Structure

Here we will go into some detail on how Babylon is structured within our project, and how we've chosen to organise the files.

---

First, we will look at the file structure for the babylon part of the game page:
```
babylon
│
├── environment
│   ├── index.ts
│   ├── camera.ts
│   ├── environment.ts
│   ├── environmentManager.ts
│   ├── light.ts
│   └── terrain.ts
│
├── entities
│   ├── index.ts
│   ├── obstacle.ts
│   ├── avatar.ts
│   └── interactable.ts
│
└── interfaces.ts
```
`interfaces.ts` contains the typing (interfaces) for objects specific to our project, such as [GameNode](../gamenode/README.md#GameNode).

We split the remaining elements of the game into two folders: 
* **environment**: The elements of the game that make up the world, such as camera, light and terrain, as well as the renderer.
* **entities**: These populate the game world, and cover elements such as obstacles, avatars, and interactables.

All classes in these folders implement the [GameNode](../gamenode/README.md#GameNode) interface.