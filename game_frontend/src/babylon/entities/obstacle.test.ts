/* eslint-env jest */
import * as BABYLON from 'babylonjs'
import { Environment } from 'babylon/environment/environment'
import Obstacle from './obstacle'
import { DiffResult } from '../diff'

class MockEnvironment implements Environment {
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

describe('obstacle', () => {
  it('adds an Obstacle parent node', () => {
    // Given
    const environment = new MockEnvironment()
    const obstacle = new Obstacle()

    // When
    obstacle.setup(environment)
    // const addList = []
    // const removeList = []
    // const editList = []
    // const diffResult = new DiffResult(addList, removeList, editList)
    // obstacle.onGameStateUpdate(diffResult)

    // Then
    const terrainNodeDescendants = environment.onTerrainNode.getDescendants()
    expect(terrainNodeDescendants.length).toBe(1)
    expect(terrainNodeDescendants[0].name).toBe('Obstacle Parent')
  })
})
