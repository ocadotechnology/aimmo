import AssetPack from './assetPack'
import {
  StandardMaterial,
  Texture,
  Color3,
  Vector3,
  TransformNode,
  Axis,
  Space,
  AbstractMesh,
  Scene,
  Color4
} from 'babylonjs'

export default class ModernAssetPack extends AssetPack {
  obstacleMaterial: StandardMaterial

  backgroundColor = new Color4(0.419, 0.678, 0.035)

  constructor (era: string, scene: Scene) {
    super(era, scene)
    this.obstacleMaterial = this.makeObstacleMaterial()
  }

  makeObstacleMaterial (): StandardMaterial {
    const material = new StandardMaterial(this.obstacleInfo.materialName, this.scene)
    // There are two different textures for the same model, but only one is used in here for now
    material.diffuseTexture = new Texture(this.obstacleInfo.textureURL, this.scene)
    material.specularColor = new Color3(0, 0, 0)
    material.diffuseColor = new Color3(0.7, 0.8, 1)
    return material
  }

  async createObstacle (
    name: string,
    location: Vector3,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    const obstacle = await super.createObstacle(name, location, parent)
    obstacle.material = this.obstacleMaterial
    obstacle.rotate(Axis.Y, this.createRandomRotation(), Space.WORLD)
    return obstacle
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
}
