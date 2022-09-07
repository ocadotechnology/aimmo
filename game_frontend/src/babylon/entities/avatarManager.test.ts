/* eslint-env jest */
import * as BABYLON from 'babylonjs'
import AvatarManager from './avatarManager'
import { DiffItem } from '../diff'
import dummyImportMesh from '../../testHelpers/dummyImportMeshAsync'
import { MockEnvironment } from '../../testHelpers/mockEnvironment'

let environment: MockEnvironment
let avatars: AvatarManager

beforeEach(() => {
  environment = new MockEnvironment(true, 'future')
  avatars = new AvatarManager(environment, dummyImportMesh)
})

function avatarDiffItem(index: number, orientation: string, location: { x: number; y: number }) {
  return new DiffItem(index, {
    health: 5,
    location: {
      x: location.x,
      y: location.y,
    },
    score: 0,
    id: index,
    orientation: orientation,
  })
}

describe('AvatarManager', () => {
  it('adds an Avatar parent node', () => {
    const terrainNodeDescendants = environment.onTerrainNode.getDescendants()
    expect(terrainNodeDescendants.length).toBe(1)
    expect(terrainNodeDescendants[0].name).toBe('Avatars')
  })

  it('adds an avatar', async () => {
    const avatar = avatarDiffItem(1, 'east', { x: 0, y: 0 })

    await avatars.add(avatar)
    const avatarNodeDescendants = avatars.avatarNode.getDescendants()
    expect(avatarNodeDescendants.length).toEqual(1)
  })

  it('removes an avatar', async () => {
    const avatar = avatarDiffItem(1, 'east', { x: 0, y: 0 })

    await avatars.add(avatar)
    let avatarNodeDescendants = avatars.avatarNode.getDescendants()
    expect(avatarNodeDescendants.length).toEqual(1)

    avatars.remove(avatar)

    avatarNodeDescendants = avatars.avatarNode.getDescendants()
    expect(avatarNodeDescendants.length).toEqual(0)
  })

  it('sets current avatar mesh if it matches the ID', async () => {
    avatars.setCurrentAvatarID(1)
    const avatar = avatarDiffItem(1, 'east', { x: 0, y: 0 })

    await avatars.add(avatar)

    const avatarNodeDescendants = avatars.avatarNode.getChildMeshes()
    expect(avatars.currentAvatarMesh).toEqual(avatarNodeDescendants[0])
  })

  it('updates existing avatars', async () => {
    const avatar = avatarDiffItem(1, 'east', { x: 0, y: 0 })
    avatars.scene.createDefaultCamera()

    await avatars.add(avatar)
    let avatarNodeDescendants = avatars.avatarNode.getChildMeshes()
    expect(avatarNodeDescendants.length).toEqual(1)
    expect(avatarNodeDescendants[0].position).toEqual(new BABYLON.Vector3(0, 0, 0))

    const updatedAvatar = avatarDiffItem(1, 'east', { x: 1, y: 0 })
    avatars.edit(updatedAvatar)

    avatarNodeDescendants = avatars.avatarNode.getChildMeshes()
    setTimeout(() => {
      expect(avatarNodeDescendants.length).toEqual(1)
      expect(avatarNodeDescendants[0].position).toEqual(new BABYLON.Vector3(1, 0, 0))
    })
  })
})
