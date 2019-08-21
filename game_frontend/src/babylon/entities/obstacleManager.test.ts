/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import ObstacleManager from './obstacleManager'
import { DiffItem } from '../diff'

let environment: MockEnvironment
let obstacles: ObstacleManager

beforeEach(() => {
  environment = new MockEnvironment()
  obstacles = new ObstacleManager(environment)
})

function obstacleDiffItem (index: string, location: {x: number, y: number}) {
  return new DiffItem(index, {
    location: { x: location.x, y: location.y },
    width: 1,
    height: 1,
    'type': 'wall',
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

    obstacles.remove(obstacle)

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

    obstacles.edit(updatedObstacle)

    meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)
    expect(meshes[0].position).toEqual({ x: 1, y: 0.5, z: 1 })
  })
})
