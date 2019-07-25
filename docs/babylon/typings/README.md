# Typings

This document outlines how we make use of Typescript within the `GameView` (Babylon) component.

---

This presumes a basic level of understanding of Javascript programming and knowledge of types.

We make use of Typescript. This means that, when creating functions or assigning attributes, these must be typed. This helps the code be self-documented.

Here are some examples:

This is an example of typing object attributes.
```Typescript
export default class Camera implements GameNode {
    object: any;
    frustum: number;
    zoom_factor: number;

```

This is an example of typing function arguments and return.
```Typescript
onSceneMount(scene: BABYLON.Scene, canvas: HTMLCanvasElement, engine: BABYLON.Engine): void {
    const camera = new BABYLON.ArcRotateCamera('camera1', 0, 0.785, 50, BABYLON.Vector3.Zero(), scene)
    this.frustum = 7.5
    this.zoom_factor = 0
    this.object = camera

    camera.mode = BABYLON.Camera.ORTHOGRAPHIC_CAMERA
    camera.orthoTop = 5
    ...
```

### GameNode

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
        