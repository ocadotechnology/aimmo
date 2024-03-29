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
  Color4,
} from 'babylonjs'

export default class PreHistoryAssetPack extends AssetPack {
  obstacleMaterials: StandardMaterial[]

  backgroundColor = new Color4(0.2, 0.35, 0.2)

  constructor(era: string, scene: Scene) {
    super(era, scene)
    this.obstacleMaterials = this.makeObstacleMaterials()
  }

  makeObstacleMaterials(): StandardMaterial[] {
    return [1, 2].map((textureChoice) => {
      const material = new StandardMaterial(
        `${this.obstacleInfo.materialName}_${textureChoice}`,
        this.scene
      )
      material.diffuseTexture = new Texture(this.getTextureURL(textureChoice), this.scene)
      material.specularColor = new Color3(0, 0, 0)
      material.diffuseColor = new Color3(0.7, 0.8, 1)
      return material
    })
  }

  async createObstacle(
    name: string,
    location: Vector3,
    textureChoice: number,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    const obstacle = await super.createObstacle(name, location, textureChoice, parent)
    obstacle.material = this.obstacleMaterials[textureChoice - 1]
    obstacle.rotate(Axis.Y, this.createRandomRotation(), Space.WORLD)
    return obstacle
  }

  /**
   * This function returns a random angle in radians
   *
   * @return {number} a random angle in radians, in increments of a quarter
   *
   */
  createRandomRotation(): number {
    return Math.PI / (Math.floor(Math.random() * Math.floor(4)) + 1)
  }
}
