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

export default class AncientAssetPack extends AssetPack {
  obstacleMaterial: StandardMaterial

  backgroundColor = new Color4(0.47, 0.47, 0.47)

  constructor (era: string, scene: Scene) {
    super(era, scene)
    this.obstacleMaterial = this.makeObstacleMaterial()
  }

  makeObstacleMaterial (): StandardMaterial {
    const material = new StandardMaterial(this.obstacleInfo.materialName, this.scene)
    material.diffuseTexture = new Texture(this.getTextureURL(1), this.scene)
    material.specularColor = new Color3(0, 0, 0)
    material.diffuseColor = new Color3(1, 1, 1)
    return material
  }

  async createObstacle (
    name: string,
    location: Vector3,
    textureChoice: number,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    // There are two different models for the same texture, but only one is used in here for now
    const obstacle = await super.createObstacle(name, location, textureChoice, parent)
    obstacle.material = this.obstacleMaterial
    return obstacle
  }
}
