# GameNode

`GameNode` is an interface for implementing the objects that are part of the game world. 

```Typescript
export interface GameNode {
    object: any
    setup(environment: Environment): void
}
```

* `object` should contain the Babylon component, such as the camera, terrain, or engine. 
* `setup` is where the component should be created with its initial settings, which it gets from the `environment` parameter.

>Remember to set `this.object` in `setup`