import { GameNode, DiffHandling, DiffProcessor } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffItem } from '../diff'
import AssetPack from '../assetPacks/assetPack'

export default class InteractableManager implements GameNode, DiffHandling {
  object: any
  assetPack: AssetPack
  interactableNode: BABYLON.TransformNode
  importMesh: Function
  materials: any
  gameStateProcessor: DiffProcessor

  constructor (
    environment: Environment,
    assetPack: AssetPack
  ) {
    this.gameStateProcessor = new DiffProcessor(this)
    this.assetPack = assetPack
    this.interactableNode = new BABYLON.TransformNode('Interactables', environment.scene)
    this.object = this.interactableNode
    this.interactableNode.parent = environment.onTerrainNode
  }

  remove (interactable: DiffItem): void {
    const index = interactable.id
    const toDelete = this.interactableNode.getChildMeshes(true, function (node): boolean {
      return node.name === `interactable: ${index}`
    })
    if (toDelete.length > 0) {
      toDelete[0].dispose()
    }
  }

  async edit (interactable: DiffItem) {
    const toEdit = this.interactableNode.getChildMeshes(true, function (node): boolean {
      return node.name === `interactable: ${interactable.id}`
    })
    if (toEdit.length > 0) {
      // if the interactable has the same type then we can change its position, otherwise we need to recreate it
      if (toEdit[0].metadata.type === interactable.value.type) {
        toEdit[0].position = new BABYLON.Vector3(
          interactable.value.location.x,
          0,
          interactable.value.location.y
        )
      }
      else {
        toEdit[0].dispose()
        await this.add(interactable)
      }
    }
  }

  async add (interactable: DiffItem) {
    await this.assetPack.createInteractable(
      `interactable: ${interactable.id}`,
      interactable.value.type,
      new BABYLON.Vector3(interactable.value.location.x, 0, interactable.value.location.y),
      this.interactableNode
    )
  }
}
