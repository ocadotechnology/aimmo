/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import Obstacle from './obstacle'
import { DiffResult } from '../diff'

let environment: MockEnvironment
let obstacle: Obstacle

beforeEach(() => {
  environment = new MockEnvironment()
  obstacle = new Obstacle()

  obstacle.setup(environment)
})

function obstacleList (positionDict) {
  let list = []

  for (let [index, position] of Object.entries(positionDict)) {
    list.push({
      id: index,
      value: {
        'location': { 'x': position[0], 'y': position[1] },
        'width': 1,
        'height': 1,
        'type': 'wall',
        'orientation': 'north'
      }
    })
  }
  return list
}

describe('obstacle', () => {
  it('adds an Obstacles node', () => {
    const terrainNodeChildren = environment.onTerrainNode.getChildren()

    expect(terrainNodeChildren.length).toBe(1)
    expect(terrainNodeChildren[0].name).toBe('Obstacles')
  })

  it('adds an obstacle', () => {
    const addList = obstacleList({ '0': [10, 10] })
    const diffResult = new DiffResult(addList, [], [])
    obstacle.onGameStateUpdate(diffResult)

    const obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)
    expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })
  })

  it('deletes an obstacle', () => {
    const addList = obstacleList({ '0': [10, 10] })
    let diffResult = new DiffResult(addList, [], [])
    obstacle.onGameStateUpdate(diffResult)

    let obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)

    const deleteList = obstacleList({ '0': [10, 10] })
    diffResult = new DiffResult([], deleteList, [])
    obstacle.onGameStateUpdate(diffResult)

    obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(0)
  })

  it('edits an obstacle', () => {
    const addList = obstacleList({ '0': [10, 10] })
    let diffResult = new DiffResult(addList, [], [])
    obstacle.onGameStateUpdate(diffResult)

    let obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)
    expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })

    const editList = obstacleList({ '0': [-7, 2] })
    diffResult = new DiffResult([], [], editList)
    obstacle.onGameStateUpdate(diffResult)

    obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(1)
    expect(obstacles[0].position).toEqual({ x: -7, y: 0.5, z: 2 })
  })

  it('adds, edits and delete obstacles on same update', () => {
    let addList = obstacleList({ '0': [10, 10], '1': [15, 15] })
    let diffResult = new DiffResult(addList, [], [])
    obstacle.onGameStateUpdate(diffResult)

    let obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(2)
    expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })
    expect(obstacles[1].position).toEqual({ x: 15, y: 0.5, z: 15 })

    addList = obstacleList({ '2': [15, 15] })
    const editList = obstacleList({ '1': [10, 10] })
    const deleteList = obstacleList({ '0': [10, 10] })
    diffResult = new DiffResult(addList, deleteList, editList)
    obstacle.onGameStateUpdate(diffResult)

    obstacles = obstacle.obstacleNode.getChildren()

    expect(obstacles.length).toBe(2)
    expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })
    expect(obstacles[1].position).toEqual({ x: 15, y: 0.5, z: 15 })
  })
})
