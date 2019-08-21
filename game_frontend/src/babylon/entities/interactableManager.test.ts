/* eslint-env jest */
import * as BABYLON from 'babylonjs'
import InteractableManager from './interactableManager'
import { DiffItem } from '../diff'
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import dummyImportMesh from '../../testHelpers/dummyImportMesh'

let environment: MockEnvironment
let interactable: InteractableManager

beforeEach(() => {
  environment = new MockEnvironment()
  interactable = new InteractableManager(environment, dummyImportMesh)
})

function interactableDiffItem (index: string, type: string, location: {x: number, y: number}) {
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

  it('adds interactables to a new Interactable', () => {
    const interactableList = [
      interactableDiffItem('1', 'score', { x: 0, y: 1 }),
      interactableDiffItem('2', 'damage_boost', { x: 1, y: 0 })
    ]

    interactable.add(interactableList[0])
    let interactableNodeDescendants = interactable.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(1)

    interactable.add(interactableList[1])
    interactableNodeDescendants = interactable.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(2)
  })

  it('removes interactables from an Interactable', () => {
    const interactableList = [
      interactableDiffItem('1', 'score', { x: 0, y: 1 }),
      interactableDiffItem('2', 'damage_boost', { x: 1, y: 0 })
    ]

    interactable.add(interactableList[0])
    interactable.add(interactableList[1])
    let interactableNodeDescendants = interactable.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(2)

    interactable.remove(interactableList[1])
    interactableNodeDescendants = interactable.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(1)
  })

  it('edits interactable from an Interactable', () => {
    const interactableItem = interactableDiffItem('1', 'score', { x: 0, y: 1 })

    interactable.add(interactableItem)

    var interactableNodeChildren = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new BABYLON.Vector3(0, 0, 1))

    const updatedInteractableItem = interactableDiffItem('1', 'score', { x: 1, y: 0 })

    interactable.edit(updatedInteractableItem)

    interactableNodeChildren = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new BABYLON.Vector3(1, 0, 0))
  })
})
