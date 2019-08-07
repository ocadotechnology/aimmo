import * as BABYLON from 'babylonjs'
import { Environment } from '../babylon/environment/environment'

export class MockEnvironment implements Environment {
  scene: BABYLON.Scene;
  engine: BABYLON.Engine;
  onTerrainNode: BABYLON.TransformNode;

  constructor () {
    this.engine = new BABYLON.NullEngine()
    this.scene = new BABYLON.Scene(this.engine)

    this.onTerrainNode = new BABYLON.TransformNode('On Terrain', this.scene)
    this.onTerrainNode.position = new BABYLON.Vector3(0.5, 0, 0.5)
  }
}
