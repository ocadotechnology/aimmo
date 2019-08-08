/* eslint-env jest */
import * as BABYLON from 'babylonjs'
import Interactable from './interactable'
import { DiffResult } from '../diff'
import { MockEnvironment } from '../../testHelpers/mockEnvironment'

let environment: MockEnvironment
let interactable: Interactable

beforeEach(() => {
  environment = new MockEnvironment()
  interactable = new Interactable(dummyImportMesh)

  interactable.setup(environment)
})

function dummyImportMesh (meshName: string, filePath: string, fileName: string, scene: BABYLON.Scene, onSuccess: Function): void {
  const meshes = []
  meshes[0] = BABYLON.MeshBuilder.CreateBox('', { height: 1 }, this.scene)

  onSuccess(meshes, [], [], [])
}

function createInteractableList (numberOfInteractables: number, interactableType: string) : any {
  var list = []
  for (let i = 0; i < numberOfInteractables; i++) {
    list[i] = {
      id: i,
      value: {
        type: interactableType,
        location: {
          x: i,
          y: i
        }
      }
    }
  }

  return list
}

describe('interactable', () => {
  it('adds an Interactable parent node', () => {
    const terrainNodeDescendants = environment.onTerrainNode.getDescendants()
    expect(terrainNodeDescendants.length).toBe(1)
    expect(terrainNodeDescendants[0].name).toBe('Interactables')
  })

  it('adds interactables to a new Interactable', () => {
    const addList = createInteractableList(2, 'score')
    const deleteList = []
    const editList = []

    const diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    const interactableNodeDescendants = interactable.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(2)
  })

  it('removes interactables from an Interactable', () => {
    var addList = createInteractableList(2, 'score')
    var deleteList = []
    const editList = []

    var diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    deleteList = [addList[1]]
    addList = []

    diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    const interactableNodeDescendants = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeDescendants.length).toBe(1)
  })

  it('edits interactable from an Interactable', () => {
    var addList = createInteractableList(1, 'score')
    const deleteList = []
    var editList = []

    var diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    var interactableNodeChildren = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new BABYLON.Vector3(0, 0, 0))

    addList[0].value.location.x = 2

    editList = [addList[0]]
    addList = []

    diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    interactableNodeChildren = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new BABYLON.Vector3(2, 0, 0))
  })

  it('adds, removes and edits interactables on a new Interactable at the same time', () => {
    const list = createInteractableList(4, 'score')
    var addList = list.slice(0, 3)
    var deleteList = []
    var editList = []

    var diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    addList = [list[3]]
    deleteList = [list[2]]
    editList = [list[0]]
    editList[0].value.location.x = 2

    diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    const interactableNodeChildren = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeChildren.length).toBe(3)
    expect(interactableNodeChildren[0].position).toEqual(new BABYLON.Vector3(2, 0, 0))
  })

  it('removes and edits the same object from an Interactable at the same time', () => {
    var addList = createInteractableList(1, 'score')
    var deleteList = []
    var editList = []

    interactable.setup(environment)

    var diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    deleteList = [addList[0]]
    editList = [addList[0]]
    editList[0].value.location.x = 2

    addList = []

    diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    const interactableNodeChildren = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeChildren.length).toBe(0)
  })
})
