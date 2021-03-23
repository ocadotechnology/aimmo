/* eslint-env jest */
import InteractableManager from './interactableManager'
import { DiffItem } from '../diff'
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import AssetPack from '../assetPacks/assetPack'
import { Vector3 } from 'babylonjs'
import dummyImportMeshAsync from 'testHelpers/dummyImportMeshAsync'

let environment: MockEnvironment
let interactableManager: InteractableManager

beforeEach(() => {
  environment = new MockEnvironment(true, 'future')
  const assetPack = new AssetPack(environment.era, environment.scene, dummyImportMeshAsync)
  interactableManager = new InteractableManager(environment, assetPack)
})

function interactableDiffItem (index: number, type: string, location: { x: number; y: number }) {
  return new DiffItem(index, {
    type: type,
    location: {
      x: location.x,
      y: location.y
    }
  })
}

describe('InteractableManager', () => {
  it('adds an Interactable parent node', () => {
    const terrainNodeDescendants = environment.onTerrainNode.getDescendants()
    expect(terrainNodeDescendants.length).toBe(1)
    expect(terrainNodeDescendants[0].name).toBe('Interactables')
  })

  it('adds interactables to a new Interactable', async () => {
    jest.spyOn(interactableManager.assetPack, 'createInteractable')
    const interactableList = [
      interactableDiffItem(1, 'score', { x: 0, y: 1 }),
      interactableDiffItem(2, 'damage_boost', { x: 1, y: 0 })
    ]

    await interactableManager.add(interactableList[0])
    expect(interactableManager.assetPack.createInteractable).toBeCalledWith(
      'interactable: 1',
      'score',
      new Vector3(0, 0, 1),
      interactableManager.object
    )
    let interactableNodeDescendants = interactableManager.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(1)

    await interactableManager.add(interactableList[1])
    expect(interactableManager.assetPack.createInteractable).toBeCalledTimes(2)
    expect(interactableManager.assetPack.createInteractable).toBeCalledWith(
      'interactable: 2',
      'damage_boost',
      new Vector3(1, 0, 0),
      interactableManager.object
    )
    interactableNodeDescendants = interactableManager.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(2)
  })

  it('removes interactables from an Interactable', async () => {
    const interactableList = [
      interactableDiffItem(1, 'score', { x: 0, y: 1 }),
      interactableDiffItem(2, 'damage_boost', { x: 1, y: 0 })
    ]

    await interactableManager.add(interactableList[0])
    await interactableManager.add(interactableList[1])
    let interactableNodeDescendants = interactableManager.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(2)

    interactableManager.remove(interactableList[1])
    interactableNodeDescendants = interactableManager.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(1)
  })

  it('edits interactable from an Interactable with the same type', async () => {
    const interactableItem = interactableDiffItem(1, 'score', { x: 0, y: 1 })

    await interactableManager.add(interactableItem)

    var interactableNodeChildren = interactableManager.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new Vector3(0, 0, 1))
    expect(interactableNodeChildren[0].metadata.type).toEqual('score')

    const updatedInteractableItem = interactableDiffItem(1, 'score', { x: 1, y: 0 })

    await interactableManager.edit(updatedInteractableItem)

    interactableNodeChildren = interactableManager.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new Vector3(1, 0, 0))
    expect(interactableNodeChildren[0].metadata.type).toEqual('score')
  })

  it('edits interactable from an Interactable with a different type', async () => {
    const interactableItem = interactableDiffItem(1, 'key', { x: 2, y: 3 })

    await interactableManager.add(interactableItem)

    var interactableNodeChildren = interactableManager.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new Vector3(2, 0, 3))
    expect(interactableNodeChildren[0].metadata.type).toEqual('key')

    const updatedInteractableItem = interactableDiffItem(1, 'chest', { x: 4, y: 1 })

    await interactableManager.edit(updatedInteractableItem)

    interactableNodeChildren = interactableManager.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new Vector3(4, 0, 1))
    expect(interactableNodeChildren[0].metadata.type).toEqual('chest')
  })
})
