import { Scene, Engine, TransformNode, Vector3 } from 'babylonjs'

export interface Environment {
  scene: Scene
  engine: Engine
  canvas?: HTMLCanvasElement
  onTerrainNode: TransformNode
  era: string
}

export class StandardEnvironment implements Environment {
  scene: Scene
  engine: Engine
  canvas: HTMLCanvasElement
  onTerrainNode: TransformNode
  era: string

  constructor (canvas: HTMLCanvasElement) {
    this.canvas = canvas
    this.engine = new Engine(this.canvas, true, {}, true)
    this.engine.enableOfflineSupport = true

    this.scene = new Scene(this.engine)

    this.onTerrainNode = new TransformNode('On Terrain', this.scene)
    this.onTerrainNode.position = new Vector3(0.5, 0, 0.5)

    this.era = ''
  }
}
