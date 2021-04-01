/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import ObstacleManager from './obstacleManager'
import dummyImportMeshAsync from '../../testHelpers/dummyImportMeshAsync'
import AssetPack from '../assetPacks/assetPack'
import { DiffItem } from '../diff'
import { Vector3 } from 'babylonjs'

let environment: MockEnvironment
let obstacles: ObstacleManager

beforeEach(() => {
  environment = new MockEnvironment(true, 'future')
  const assetPack = new AssetPack(environment.era, environment.scene, dummyImportMeshAsync)
  obstacles = new ObstacleManager(environment, assetPack)
})

function obstacleDiffItem (index: number, location: {x: number; y: number}) {
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

  it('adds an obstacle', async () => {
    const obstacle = obstacleDiffItem(1, { x: 0, y: 0 })
    await obstacles.add(obstacle)

    const meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)
    expect(meshes[0].position).toEqual(new Vector3(0, 0, 0))
  })

  it('deletes an obstacle', async () => {
    const obstacle = obstacleDiffItem(1, { x: 0, y: 0 })
    await obstacles.add(obstacle)

    let meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)

    obstacles.remove(obstacle)

    meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(0)
  })

  it('updates an obstacle', async () => {
    const obstacle = obstacleDiffItem(1, { x: 0, y: 0 })
    await obstacles.add(obstacle)

    let meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)
    expect(meshes[0].position).toEqual(new Vector3(0, 0, 0))

    const updatedObstacle = obstacleDiffItem(1, { x: 1, y: 1 })

    obstacles.edit(updatedObstacle)

    meshes = obstacles.obstacleNode.getChildMeshes()

    expect(meshes.length).toBe(1)
    expect(meshes[0].position).toEqual(new Vector3(1, 0, 1))
  })
})
