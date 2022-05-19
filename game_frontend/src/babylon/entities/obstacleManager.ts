import { GameNode, DiffHandling, DiffProcessor } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { DiffItem } from '../diff'
import AssetPack from '../assetPacks/assetPack'
import { Environment } from '../environment/environment'

export default class ObstacleManager implements GameNode, DiffHandling {
  object: any
  obstacleNode: BABYLON.TransformNode
  gameStateProcessor: DiffProcessor
  importMesh: Function
  materials: Array<BABYLON.StandardMaterial>
  assetPack: AssetPack

  constructor(environment: Environment, assetPack: AssetPack) {
    this.assetPack = assetPack
    this.gameStateProcessor = new DiffProcessor(this)
    this.obstacleNode = new BABYLON.TransformNode('Obstacles', environment.scene)
    this.object = this.obstacleNode
    this.obstacleNode.parent = environment.onTerrainNode
  }

  remove(obstacle: DiffItem): void {
    const index = obstacle.id
    const toDelete = this.obstacleNode.getChildMeshes(true, function (node): boolean {
      return node.name === `obstacle: ${index}`
    })
    if (toDelete.length > 0) {
      toDelete[0].dispose()
    }
  }

  edit(obstacle: DiffItem): void {
    const toEdit = this.obstacleNode.getChildMeshes(true, function (node): boolean {
      return node.name === `obstacle: ${obstacle.id}`
    })
    if (toEdit.length > 0) {
      toEdit[0].position = new BABYLON.Vector3(
        obstacle.value.location.x,
        0,
        obstacle.value.location.y
      )
    }
  }

  async add(obstacle: DiffItem) {
    await this.assetPack.createObstacle(
      `obstacle: ${obstacle.id}`,
      new BABYLON.Vector3(obstacle.value.location.x, 0, obstacle.value.location.y),
      obstacle.value.texture,
      this.obstacleNode
    )
  }
}
