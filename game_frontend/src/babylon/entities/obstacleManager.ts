import { GameNode, DiffHandling, DiffProcessor } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffItem } from '../diff'
import { AssetPack } from '../assetPack'

export default class ObstacleManager implements GameNode, DiffHandling {
  object: any
  scene: BABYLON.Scene
  obstacleNode: BABYLON.TransformNode
  gameStateProcessor: DiffProcessor
  importMesh: Function
  materials: Array <BABYLON.StandardMaterial>
  assets: AssetPack
  era: string

  constructor (environment: Environment, importMesh: Function = BABYLON.SceneLoader.ImportMesh) {
    this.gameStateProcessor = new DiffProcessor(this)
    this.era = environment.era

    this.importMesh = importMesh
    this.scene = environment.scene

    this.obstacleNode = new BABYLON.TransformNode('Obstacles', environment.scene)
    this.object = this.obstacleNode
    this.obstacleNode.parent = environment.onTerrainNode

    this.assets = new AssetPack(this.era)

    this.materials = []
    this.createMaterials()
  }

  createMaterials () {
    // Base material
    this.materials[0] = new BABYLON.StandardMaterial(this.assets.obstacles.materialName, this.scene)
    this.materials[0].diffuseTexture = new BABYLON.Texture(this.assets.obstacles.textureURL, this.scene)
    this.materials[0].specularColor = new BABYLON.Color3(0, 0, 0)
    this.materials[0].diffuseColor = new BABYLON.Color3(1, 1, 1)

    if (this.era === 'prehistory') {
      // Other materials - only one for now
      this.materials[1] = new BABYLON.StandardMaterial(this.assets.obstacles.materialName + this.era, this.scene)
      this.materials[1].diffuseTexture = new BABYLON.Texture(this.assets.obstacles.textureURL, this.scene)
      this.materials[1].specularColor = new BABYLON.Color3(0, 0, 0)
      this.materials[1].diffuseColor = new BABYLON.Color3(0.70, 0.80, 1)
    }
  }

  /**
   * This function returns a random angle in radians
   *
   * @return {number} a random angle in radians, in increments of a quarter
   *
   */
  createRandomRotation (): number {
    return Math.PI / (Math.floor(Math.random() * Math.floor(4)) + 1)
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
      toEdit[0].position = new BABYLON.Vector3(obstacle.value.location.x, 0, obstacle.value.location.y)
    }
  }

  add (obstacle: DiffItem): void {
    this.importMesh(this.assets.obstacles.name, this.assets.obstacles.modelURL, this.assets.obstacles.modelName, this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
      var newObstacle = meshes[0]
      newObstacle.name = `obstacle: ${obstacle.id}`

      newObstacle.material = this.materials[Math.floor(Math.random() * Math.floor(this.materials.length))]

      newObstacle.parent = this.obstacleNode
      newObstacle.position = new BABYLON.Vector3(obstacle.value.location.x, 0, obstacle.value.location.y)


      newObstacle.rotate(BABYLON.Axis.Y, this.createRandomRotation(), BABYLON.Space.WORLD)
    })
  }
}
