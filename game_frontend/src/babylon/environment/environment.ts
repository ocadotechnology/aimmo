import { Scene, Engine, TransformNode, Vector3 } from 'babylonjs'

export default class Environment {
    scene: Scene
    engine: Engine
    canvas: HTMLCanvasElement
    onTerrainNode: TransformNode

    constructor (canvas: HTMLCanvasElement) {
      this.canvas = canvas
    }

    setup (): void {
      this.engine = new Engine(
        this.canvas,
        true,
        {},
        true
      )

      this.scene = new Scene(this.engine)

      this.onTerrainNode = new TransformNode('On Terrain', this.scene)
      this.onTerrainNode.position = new Vector3(0.5, 0, 0.5)
    }
}
