import { GameNode, DiffHandling } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffResult } from '../diff'

export default class ObstacleManager implements GameNode, DiffHandling {
  object: any
  scene: BABYLON.Scene
  obstacleNode: BABYLON.TransformNode

  setup (environment: Environment): void {
    this.scene = environment.scene
    this.obstacleNode = new BABYLON.TransformNode('Obstacles', environment.scene)
    this.obstacleNode.parent = environment.onTerrainNode
  }

  handleDifferences (differences: DiffResult): void {
    for (let obstacle of differences.deleteList) {
      this.deleteObstacle(obstacle.id)
    }
    for (let obstacle of differences.editList) {
      this.editObstacle(obstacle)
    }
    for (let obstacle of differences.addList) {
      this.addObstacle(obstacle)
    }
  }

  deleteObstacle (index: any): void {
    const toDelete = this.obstacleNode.getChildMeshes(true,
      function (node): boolean {
        return node.name === `obstacle: ${index}`
      }
    )
    if (toDelete.length > 0) {
      toDelete[0].dispose()
    }
  }

  editObstacle (obstacle: any): void {
    const toEdit = this.obstacleNode.getChildMeshes(true,
      function (node): boolean {
        return node.name === `obstacle: ${obstacle.id}`
      }
    )
    if (toEdit.length > 0) {
      toEdit[0].position = new BABYLON.Vector3(obstacle.value.location.x, 0.5, obstacle.value.location.y)
    }
  }

  addObstacle (obstacle: any): void {
    // Create mesh
    const box = BABYLON.MeshBuilder.CreateBox(`obstacle: ${obstacle.id}`, { height: 1 }, this.scene)

    // Create and assign material
    const material = new BABYLON.StandardMaterial('obstacle_material_future', this.scene)
    material.diffuseTexture = new BABYLON.Texture('/static/images/obstacle_future_wall1.jpg', this.scene)
    box.material = material

    // Set parent and relative position
    box.parent = this.obstacleNode
    box.position = new BABYLON.Vector3(obstacle.value.location.x, 0.5, obstacle.value.location.y)
  }
}
