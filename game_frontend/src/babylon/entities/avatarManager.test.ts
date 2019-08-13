/* eslint-env jest */
import * as BABYLON from 'babylonjs'
import AvatarManager from './avatarManager'
import { DiffItem } from '../diff'
import dummyImportMesh from '../../testHelpers/dummyImportMesh'
import { MockEnvironment } from '../../testHelpers/mockEnvironment'

let environment: MockEnvironment
let avatars: AvatarManager

beforeEach(() => {
  environment = new MockEnvironment()
  avatars = new AvatarManager(dummyImportMesh)

  avatars.setup(environment)
})

function avatarDiffItem (index: string, orientation: string, location: {x: number, y: number}) {
  return new DiffItem(index, {
    health: 5,
    location: {
      x: location.x,
      y: location.y
    },
    score: 0,
    id: parseInt(index),
    orientation: orientation
  })
}

describe('avatar', () => {
  it('adds an Avatar parent node', () => {
    const terrainNodeDescendants = environment.onTerrainNode.getDescendants()
    expect(terrainNodeDescendants.length).toBe(1)
    expect(terrainNodeDescendants[0].name).toBe('Avatars')
  })

  it('adds an avatar', () => {
    const avatar = avatarDiffItem('1', 'east', { x: 0, y: 0 })

    avatars.add(avatar)
    let avatarNodeDescendants = avatars.avatarNode.getDescendants()
    expect(avatarNodeDescendants.length).toEqual(1)
  })

  it('removes an avatar', () => {
    const avatar = avatarDiffItem('1', 'east', { x: 0, y: 0 })

    avatars.add(avatar)
    let avatarNodeDescendants = avatars.avatarNode.getDescendants()
    expect(avatarNodeDescendants.length).toEqual(1)

    avatars.delete(avatar)

    avatarNodeDescendants = avatars.avatarNode.getDescendants()
    expect(avatarNodeDescendants.length).toEqual(0)
  })

  it('updates existing avatars', () => {
    const avatar = avatarDiffItem('1', 'east', { x: 0, y: 0 })

    avatars.add(avatar)
    let avatarNodeDescendants = avatars.avatarNode.getDescendants()
    expect(avatarNodeDescendants.length).toEqual(1)
    expect(avatarNodeDescendants[0].position).toEqual(new BABYLON.Vector3(0, 0, 0))

    const updatedAvatar = avatarDiffItem('1', 'east', { x: 1, y: 0 })

    avatars.edit(updatedAvatar)
    avatarNodeDescendants = avatars.avatarNode.getDescendants()
    expect(avatarNodeDescendants.length).toEqual(1)
    expect(avatarNodeDescendants[0].position).toEqual(new BABYLON.Vector3(0, 0, 0))

    avatars.edit(avatar)
  })
})