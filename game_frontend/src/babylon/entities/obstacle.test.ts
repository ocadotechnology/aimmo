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

let environment
let obstacle

beforeEach(() => {
  environment = new MockEnvironment()
  obstacle = new Obstacle()

  obstacle.setup(environment)

  addInitialObstacle()
})

function addInitialObstacle () {
  const addList = [{ id: '0',
    value: {
      'location': { 'x': 10, 'y': 10 },
      'width': 1,
      'height': 1,
      'type': 'wall',
      'orientation': 'north' }
  }]
  const diffResult = new DiffResult(addList, [], [])
  obstacle.onGameStateUpdate(diffResult)
}

describe('obstacle', () => {
  it('adds an Obstacle parent node', () => {
    const terrainNodeDescendants = environment.onTerrainNode.getChildren()

    expect(terrainNodeDescendants.length).toBe(1)
    expect(terrainNodeDescendants[0].name).toBe('Obstacle Parent')
  })

  it('adds an obstacle', () => {
    const obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)
  })

  it('deletes an obstacle', () => {
    let obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)

    const removeList = [{ id: '0',
      value: {
        'location': { 'x': 10, 'y': 10 },
        'width': 1,
        'height': 1,
        'type': 'wall',
        'orientation': 'north' }
    }]
    const diffResult = new DiffResult([], removeList, [])
    obstacle.onGameStateUpdate(diffResult)

    obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(0)
  })

  it('edits an obstacle', () => {
    let obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)
    expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })

    const editList = [{ id: '0',
      value: {
        'location': { 'x': -7, 'y': 2 },
        'width': 1,
        'height': 1,
        'type': 'wall',
        'orientation': 'north' }
    }]
    const diffResult = new DiffResult([], [], editList)
    obstacle.onGameStateUpdate(diffResult)

    obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)
    expect(obstacles[0].position).toEqual({ x: -7, y: 0.5, z: 2 })
  })
})
