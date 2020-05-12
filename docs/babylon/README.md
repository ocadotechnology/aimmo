# Babylon

This section describes the way Babylon is used as the game engine for Kurono.

---

## Structure

Here we will go into some detail on how Babylon is structured within our project, and how we've chosen to organise the files.

First, we will look at the file structure for the babylon part of the game page:
```
babylon
│
├── assetPacks
│   ├── assetPack.ts
│   ├── future.ts
│   ├── ...
│   └── getAssetPackForEra.ts
|
├── entities
│   ├── avatarManager.test.ts
│   ├── avatarManager.ts
│   ├── ...
│   └── index.ts
│
├── environment
│   ├── index.ts
│   ├── light.test.ts
│   ├── light.ts
│   ├── ...
│   ├── environment.ts
│   └── environmentManager.ts
│
├── animation.ts
├── diff.ts
├── gameEngine.ts
├── ...
├── interfaces.ts
└── orientation.ts
```
`interfaces.ts` contains the typing (interfaces) for objects specific to our project, such as `GameNode`.

We split the remaining elements of the game into two folders: 
* **entities**: These populate the game world, and cover elements such as obstacles, avatars, and interactables.
* **environment**: The elements of the game that make up the world, such as camera, light and terrain, as well as the renderer.

The files inside **assetPacks** handle the loading and processing different 2D and 3D assets required for each different level, or *era*, of the game. *NOTE: the way this is currently written, each era has one only type of obstacle. However, as pointed out in the corresponding files, there are different textures and models ready to be loaded when the randomising functionality is implemented.*

All classes in these folders implement the `GameNode` interface. Entities also implement the `DiffHandling` interface.
