import {
  StandardMaterial,
  Texture,
  Color3,
  Vector3,
  TransformNode,
  AbstractMesh,
  Scene,
  Color4
} from 'babylonjs'
import AssetPack from './assetPack'

export default class FutureAssetPack extends AssetPack {
  obstacleMaterial: StandardMaterial

  backgroundColor = new Color4(0.69, 0.729, 0.988)

  constructor (era: string, scene: Scene) {
    super(era, scene)
    this.obstacleMaterial = this.makeObstacleMaterial()
  }

  makeObstacleMaterial (): StandardMaterial {
    const material = new StandardMaterial(this.obstacleInfo.materialName, this.scene)
    material.diffuseTexture = new Texture(this.obstacleInfo.textureURL, this.scene)
    material.specularColor = new Color3(0, 0, 0)
    material.diffuseColor = new Color3(1, 1, 1)
    return material
  }

  async createObstacle (
    name: string,
    location: Vector3,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    const obstacle = await super.createObstacle(name, location, parent)
    obstacle.material = this.obstacleMaterial
    return obstacle
  }
}
