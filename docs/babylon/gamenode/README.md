# GameNode

`GameNode` is an interface for implementing the objects that are part of the game world. 

```Typescript
export interface GameNode {
    object: any
    onSceneMount(scene: Scene, canvas: HTMLCanvasElement, engine: Engine): void
    onGameStateUpdate(): void
}
```

* `object` should contain the Babylon component, such as the camera, terrain, or engine. 
* `onSceneMount` is where the component should be created with all the initial settings, see the `onSceneMount` example for the camera above. This gets called once, when the webpage is loaded. The function must be defined as shown in the code snippet above.
* `onGameStateUpdate` is where the component gets updated according to changes in the game state. This gets called whenever a new game state is received from the server. Again, the function must be defined as shown in the code snippet above.

>Remember to set `this.object` in `onSceneMount`