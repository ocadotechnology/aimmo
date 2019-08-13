/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import ObstacleManager from './obstacleManager'
import { DiffItem } from '../diff'

let environment: MockEnvironment
let obstacles: ObstacleManager

beforeEach(() => {
  environment = new MockEnvironment()
  obstacles = new ObstacleManager()

  obstacles.setup(environment)
})

function obstacleDiffItem (index: string, location: {x: number, y: number}) {
  return new DiffItem(index, {
    location: { x: location.x, y: location.y },
    width: 1,
    height: 1,
    type: 'wall',
    orientation: 'north'
  })
}

describe('obstacle', () => {
  it('adds an Obstacles node', () => {
    const terrainNodeChildren = environment.onTerrainNode.getChildren()

    expect(terrainNodeChildren.length).toBe(1)
    expect(terrainNodeChildren[0].name).toBe('Obstacles')
  })

  it('adds an obstacle', () => {
    const obstacle = obstacleDiffItem('1', { x: 0, y: 0 })
    obstacles.add(obstacle)

    const meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)
    expect(meshes[0].position).toEqual({ x: 0, y: 0.5, z: 0 })
  })

  it('deletes an obstacle', () => {
    const obstacle = obstacleDiffItem('1', { x: 0, y: 0 })
    obstacles.add(obstacle)

    let meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)

    obstacles.delete(obstacle)

    meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(0)
  })

  it('updates an obstacle', () => {
    const obstacle = obstacleDiffItem('1', { x: 0, y: 0 })
    obstacles.add(obstacle)

    let meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)
    expect(meshes[0].position).toEqual({ x: 0, y: 0.5, z: 0 })

    const updatedObstacle = obstacleDiffItem('1', { x: 1, y: 1 })

    obstacles.update(updatedObstacle)

    meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)
    expect(meshes[0].position).toEqual({ x: 1, y: 0.5, z: 1 })
  })

  // it('adds, edits and delete obstacles on same update', () => {
  //   let addList = obstacleList({ '0': [10, 10], '1': [15, 15] })
  //   let diffResult = new DiffResult(addList, [], [])
  //   obstacle.handleDifferences(diffResult)

  //   let obstacles = obstacle.obstacleNode.getChildMeshes()

  //   expect(obstacles.length).toBe(2)
  //   expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })
  //   expect(obstacles[1].position).toEqual({ x: 15, y: 0.5, z: 15 })

  //   addList = obstacleList({ '2': [15, 15] })
  //   const editList = obstacleList({ '1': [10, 10] })
  //   const deleteList = obstacleList({ '0': [10, 10] })
  //   diffResult = new DiffResult(addList, deleteList, editList)
  //   obstacle.handleDifferences(diffResult)

  //   obstacles = obstacle.obstacleNode.getChildMeshes()

  //   expect(obstacles.length).toBe(2)
  //   expect(obstacles[0].position).toEqual({ x: 10, y: 0.5, z: 10 })
  //   expect(obstacles[1].position).toEqual({ x: 15, y: 0.5, z: 15 })
  // })
})
