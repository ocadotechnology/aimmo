/* eslint-env jest */
import * as BABYLON from 'babylonjs'
import { Environment } from 'babylon/environment/environment'
import Interactable from './interactable'
import { DiffResult } from '../diff'

class MockEnvironment implements Environment {
    scene: BABYLON.Scene;
    engine: BABYLON.Engine;
    onTerrainNode: BABYLON.TransformNode;

    constructor () {
      this.engine = new BABYLON.NullEngine()
      this.scene = new BABYLON.Scene(this.engine)

      this.onTerrainNode = new BABYLON.TransformNode('On Terrain', this.scene)
      this.onTerrainNode.position = new BABYLON.Vector3(0.5, 0, 0.5)
    }

    dummyMeshImport (meshName: string, filePath: string, fileName: string, scene: BABYLON.Scene, onSuccess: Function): void {
      const meshes = []
      meshes[0] = BABYLON.MeshBuilder.CreateBox('', { height: 1 }, this.scene)

      onSuccess(meshes, [], [], [])
    }
}

describe('interactable', () => {
  it('adds an Interactable parent node', () => {
    // Given
    const environment = new MockEnvironment()
    const interactable = new Interactable()

    // When
    interactable.setup(environment)

    // Then
    const terrainNodeDescendants = environment.onTerrainNode.getDescendants()
    expect(terrainNodeDescendants.length).toBe(1)
    expect(terrainNodeDescendants[0].name).toBe('Interactable Parent')
  })

  it('adds interactables to a new Interactable', () => {
    // Given
    const environment = new MockEnvironment()
    const interactable = new Interactable(environment.dummyMeshImport)
    const addList = [
      {
        id: 0,
        value: {
          type: 'score',
          location: {
            x: 1,
            y: 1
          }
        }
      },
      {
        id: 1,
        value: {
          type: 'score',
          location: {
            x: 2,
            y: 2
          }
        }
      }
    ]
    const deleteList = []
    const editList = []

    // When
    interactable.setup(environment)

    const diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    // Then
    const interactableNodeDescendants = interactable.interactableNode.getDescendants()
    expect(interactableNodeDescendants.length).toBe(2)
  })

  it('removes interactables from an Interactable', () => {
    // Given
    const environment = new MockEnvironment()
    const interactable = new Interactable(environment.dummyMeshImport)
    const interactable0 = {
      id: 0,
      value: {
        type: 'score',
        location: {
          x: 1,
          y: 1
        }
      }
    }
    const interactable1 =
    {
      id: 1,
      value: {
        type: 'score',
        location: {
          x: 2,
          y: 2
        }
      }
    }
    var addList = [interactable0, interactable1]
    var deleteList = []
    const editList = []

    // When
    interactable.setup(environment)

    var diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    addList = []
    deleteList = [interactable1]

    diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    // Then
    const interactableNodeDescendants = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeDescendants.length).toBe(1)
  })

  it('edits interactable from an Interactable', () => {
    // Given
    const environment = new MockEnvironment()
    const interactable = new Interactable(environment.dummyMeshImport)
    var interactable0 = {
      id: 0,
      value: {
        type: 'score',
        location: {
          x: 1,
          y: 1
        }
      }
    }
    var addList = [interactable0]
    const deleteList = []
    var editList = []

    // When
    interactable.setup(environment)

    var diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    var interactableNodeChildren = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new BABYLON.Vector3(1, 0.5, 1))

    interactable0.value.location.x = 2

    addList = []
    editList = [interactable0]

    diffResult = new DiffResult(addList, deleteList, editList)
    interactable.onGameStateUpdate(diffResult)

    // Then
    interactableNodeChildren = interactable.interactableNode.getChildMeshes()
    expect(interactableNodeChildren[0].position).toEqual(new BABYLON.Vector3(2, 0.5, 1))
  })
})
