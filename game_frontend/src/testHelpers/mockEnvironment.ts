import * as BABYLON from 'babylonjs'
import { Environment } from '../babylon/environment/environment'

/**
 * Class which mocks the Environment class. This uses the BABYLON NullEngine
 * so we can test different elements from Babylon without needing a canvas.
 *
 * The class still has a canvas property however, but it is not instantiated
 * in the constructor. This is because some elements might still require the
 * presence of a canvas to be loaded properly, like the Camera. In thi case,
 * we mock the canvas element using jest.
 */
export class MockEnvironment implements Environment {
  scene: BABYLON.Scene;
  engine: BABYLON.Engine;
  canvas: HTMLCanvasElement;
  onTerrainNode: BABYLON.TransformNode;

  constructor () {
    this.engine = new BABYLON.NullEngine()
    this.scene = new BABYLON.Scene(this.engine)

    this.onTerrainNode = new BABYLON.TransformNode('On Terrain', this.scene)
    this.onTerrainNode.position = new BABYLON.Vector3(0.5, 0, 0.5)
  }
}
