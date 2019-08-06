/* eslint-env jest */
import { MockEnvironment } from '../environment/environment.test'
import Obstacle from './obstacle'
import { DiffResult } from '../diff'

let environment: MockEnvironment
let obstacle: Obstacle

beforeEach(() => {
  environment = new MockEnvironment()
  obstacle = new Obstacle()

  obstacle.setup(environment)

  addInitialObstacle('0', 10, 10)
})

function addInitialObstacle (id: string, posX: number, posY: number) {
  const addList = [{ id: id,
    value: {
      'location': { 'x': posX, 'y': posY },
      'width': 1,
      'height': 1,
      'type': 'wall',
      'orientation': 'north' }
  }]
  const diffResult = new DiffResult(addList, [], [])
  obstacle.onGameStateUpdate(diffResult)
}

describe('obstacle', () => {
  it('adds an Obstacles node', () => {
    const terrainNodeChildren = environment.onTerrainNode.getChildren()

    expect(terrainNodeChildren.length).toBe(1)
    expect(terrainNodeChildren[0].name).toBe('Obstacles')
  })

  it('adds an obstacle', () => {
    const obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)
  })

  it('deletes an obstacle', () => {
    let obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)

    const deleteList = [{ id: '0',
      value: {
        'location': { 'x': 10, 'y': 10 },
        'width': 1,
        'height': 1,
        'type': 'wall',
        'orientation': 'north' }
    }]
    const diffResult = new DiffResult([], deleteList, [])
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

  it('adds, edits and delete obstacles on same update', () => {
    addInitialObstacle('1', 15, 15)

    let obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(2)
    expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })
    expect(obstacles[1].position).toEqual({ x: 15, y: 0.5, z: 15 })

    const addList = [{ id: '2',
      value: {
        'location': { 'x': 15, 'y': 15 },
        'width': 1,
        'height': 1,
        'type': 'wall',
        'orientation': 'north' }
    }]
    const editList = [{ id: '1',
      value: {
        'location': { 'x': 10, 'y': 10 },
        'width': 1,
        'height': 1,
        'type': 'wall',
        'orientation': 'north' }
    }]
    const deleteList = [{ id: '0',
      value: {
        'location': { 'x': 10, 'y': 10 },
        'width': 1,
        'height': 1,
        'type': 'wall',
        'orientation': 'north' }
    }]
    const diffResult = new DiffResult(addList, deleteList, editList)
    obstacle.onGameStateUpdate(diffResult)

    obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(2)
    expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })
    expect(obstacles[1].position).toEqual({ x: 15, y: 0.5, z: 15 })
  })
})
