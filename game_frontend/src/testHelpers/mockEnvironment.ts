import * as BABYLON from 'babylonjs'
import { Environment } from '../babylon/environment/environment'

/**
 * Class which provides a mock implementation of the Environment interface.
 * This uses the BABYLON NullEngine so we can test different elements from
 * Babylon without needing a canvas.
 */
export class MockEnvironment implements Environment {
  scene: BABYLON.Scene;
  engine: BABYLON.Engine;
  canvas: HTMLCanvasElement;
  onTerrainNode: BABYLON.TransformNode;

  constructor (useCanvas: boolean = false) {
    this.engine = new BABYLON.NullEngine()
    this.scene = new BABYLON.Scene(this.engine)

    if (useCanvas) {
      this.canvas = document.createElement('canvas')
    }

    this.onTerrainNode = new BABYLON.TransformNode('On Terrain', this.scene)
    this.onTerrainNode.position = new BABYLON.Vector3(0.5, 0, 0.5)
  }
}
