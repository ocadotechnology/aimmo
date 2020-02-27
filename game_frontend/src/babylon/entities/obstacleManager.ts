import { GameNode, DiffHandling, DiffProcessor } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffItem } from '../diff'

export default class ObstacleManager implements GameNode, DiffHandling {
  object: any
  scene: BABYLON.Scene
  obstacleNode: BABYLON.TransformNode
  gameStateProcessor: DiffProcessor
  importMesh: Function
  materials: Array <BABYLON.StandardMaterial>
  timeline: String

  constructor (environment: Environment, importMesh: Function = BABYLON.SceneLoader.ImportMesh) {
    this.gameStateProcessor = new DiffProcessor(this)

    this.importMesh = importMesh
    this.timeline = environment.timeline
    this.scene = environment.scene

    this.obstacleNode = new BABYLON.TransformNode('Obstacles', environment.scene)
    this.object = this.obstacleNode
    this.obstacleNode.parent = environment.onTerrainNode

    this.materials = []
    this.createMaterials()
  }

  createMaterials () {
    const textureUrl = '/static/babylon/obstacles/obstacle_' + this.timeline + '.jpg'

    // Base material
    this.materials[0] = new BABYLON.StandardMaterial('obstacle_material_' + this.timeline, this.scene)
    this.materials[0].diffuseTexture = new BABYLON.Texture(textureUrl, this.scene)
    this.materials[0].specularColor = new BABYLON.Color3(0, 0, 0)
    this.materials[0].diffuseColor = new BABYLON.Color3(1, 1, 1)

    if (this.timeline === 'prehistory') {
      // Other materials - only one for now
      this.materials[1] = new BABYLON.StandardMaterial('obstacle_material_' + this.timeline, this.scene)
      this.materials[1].diffuseTexture = new BABYLON.Texture(textureUrl, this.scene)
      this.materials[1].specularColor = new BABYLON.Color3(0, 0, 0)
      this.materials[1].diffuseColor = new BABYLON.Color3(0.70, 0.80, 1)
    }
  }

  createRandomRotation (): number {
    return Math.PI / (Math.floor(Math.random() * Math.floor(4)))
  }

  remove (obstacle: DiffItem): void {
    const index = obstacle.id
    const toDelete = this.obstacleNode.getChildMeshes(true,
      function (node): boolean {
        return node.name === `obstacle: ${index}`
      }
    )
    if (toDelete.length > 0) {
      toDelete[0].dispose()
    }
  }

  edit (obstacle: DiffItem): void {
    const toEdit = this.obstacleNode.getChildMeshes(true,
      function (node): boolean {
        return node.name === `obstacle: ${obstacle.id}`
      }
    )
    if (toEdit.length > 0) {
      toEdit[0].position = new BABYLON.Vector3(obstacle.value.location.x, 0.5, obstacle.value.location.y)
    }
  }

  add (obstacle: DiffItem): void {
    if (this.timeline === 'prehistory') {
      this.importMesh('rock', '/static/babylon/obstacles/', 'rock_model.babylon', this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
        var newObstacle = meshes[0]
        newObstacle.name = `obstacle: ${obstacle.id}`

        newObstacle.material = this.materials[Math.floor(Math.random() * Math.floor(this.materials.length))]

        newObstacle.parent = this.obstacleNode
        newObstacle.position = new BABYLON.Vector3(obstacle.value.location.x, 0, obstacle.value.location.y)

        newObstacle.rotate(BABYLON.Axis.Y, this.createRandomRotation(), BABYLON.Space.WORLD)
      })
    } else {
      var newObstacle = BABYLON.MeshBuilder.CreateBox(`obstacle: ${obstacle.id}`, { height: 1 }, this.scene)
      newObstacle.material = this.materials[0]

      newObstacle.parent = this.obstacleNode
      newObstacle.position = new BABYLON.Vector3(obstacle.value.location.x, 0.5, obstacle.value.location.y)
    }
  }
}
